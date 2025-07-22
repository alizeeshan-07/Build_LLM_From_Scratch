import os
import ast
import re
from typing import Dict, List, Tuple, Optional
from pathlib import Path

def get_type_annotation_str(annotation):
    """Convert type annotation to readable string."""
    if annotation is None:
        return "Any"
    
    if isinstance(annotation, ast.Name):
        return annotation.id
    elif isinstance(annotation, ast.Constant):
        return str(annotation.value)
    elif isinstance(annotation, ast.Attribute):
        return f"{get_type_annotation_str(annotation.value)}.{annotation.attr}"
    elif isinstance(annotation, ast.Subscript):
        value = get_type_annotation_str(annotation.value)
        slice_val = get_type_annotation_str(annotation.slice)
        return f"{value}[{slice_val}]"
    elif isinstance(annotation, ast.Tuple):
        elements = [get_type_annotation_str(elt) for elt in annotation.elts]
        return f"({', '.join(elements)})"
    elif isinstance(annotation, ast.List):
        elements = [get_type_annotation_str(elt) for elt in annotation.elts]
        return f"[{', '.join(elements)}]"
    else:
        return "Any"

def extract_function_info(node):
    """Extract detailed function information including parameters and return type."""
    func_info = {
        'name': node.name,
        'docstring': ast.get_docstring(node) or 'No description available',
        'parameters': [],
        'return_type': 'Any'
    }
    
    # Extract parameters
    for arg in node.args.args:
        param_info = {
            'name': arg.arg,
            'type': get_type_annotation_str(arg.annotation) if arg.annotation else 'Any',
            'default': None
        }
        func_info['parameters'].append(param_info)
    
    # Extract default values
    defaults = node.args.defaults
    if defaults:
        num_defaults = len(defaults)
        num_params = len(func_info['parameters'])
        start_idx = num_params - num_defaults
        
        for i, default in enumerate(defaults):
            param_idx = start_idx + i
            if isinstance(default, ast.Constant):
                func_info['parameters'][param_idx]['default'] = repr(default.value)
            elif isinstance(default, ast.Name):
                func_info['parameters'][param_idx]['default'] = default.id
            else:
                func_info['parameters'][param_idx]['default'] = 'default_value'
    
    # Extract return type
    if node.returns:
        func_info['return_type'] = get_type_annotation_str(node.returns)
    
    return func_info

def extract_class_info(node):
    """Extract class information including methods."""
    class_info = {
        'name': node.name,
        'docstring': ast.get_docstring(node) or 'No description available',
        'methods': []
    }
    
    for item in node.body:
        if isinstance(item, ast.FunctionDef):
            method_info = extract_function_info(item)
            method_info['is_private'] = item.name.startswith('_')
            method_info['is_constructor'] = item.name == '__init__'
            class_info['methods'].append(method_info)
    
    return class_info

def parse_docstring_sections(docstring):
    """Parse docstring to extract parameter descriptions and return information."""
    if not docstring:
        return {}, None
    
    lines = docstring.split('\n')
    param_descriptions = {}
    return_description = None
    current_section = None
    
    for line in lines:
        line = line.strip()
        
        if line.lower().startswith(('args:', 'parameters:', 'params:')):
            current_section = 'params'
            continue
        elif line.lower().startswith(('returns:', 'return:')):
            current_section = 'returns'
            continue
        elif line.lower().startswith(('raises:', 'examples:', 'note:', 'notes:')):
            current_section = 'other'
            continue
        
        if current_section == 'params' and ':' in line:
            param_match = re.match(r'^\s*(\w+)(?:\s*\([^)]+\))?\s*:\s*(.+)', line)
            if param_match:
                param_name, description = param_match.groups()
                param_descriptions[param_name] = description.strip()
        
        elif current_section == 'returns' and line:
            if not return_description:
                return_description = line
            else:
                return_description += ' ' + line
    
    return param_descriptions, return_description

def analyze_python_file(file_path: str):
    """Analyze a Python file and extract all relevant information."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            tree = ast.parse(content)
    except (SyntaxError, UnicodeDecodeError) as e:
        return {
            'module_docstring': f'Error parsing file: {str(e)}',
            'functions': [],
            'classes': [],
            'imports': []
        }
    
    result = {
        'module_docstring': ast.get_docstring(tree),
        'functions': [],
        'classes': [],
        'imports': []
    }
    
    # Extract imports
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                result['imports'].append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                result['imports'].append(f"{module}.{alias.name}" if module else alias.name)
    
    # Extract top-level functions and classes
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            func_info = extract_function_info(node)
            param_descriptions, return_description = parse_docstring_sections(func_info['docstring'])
            func_info['param_descriptions'] = param_descriptions
            func_info['return_description'] = return_description
            result['functions'].append(func_info)
        
        elif isinstance(node, ast.ClassDef):
            class_info = extract_class_info(node)
            result['classes'].append(class_info)
    
    return result

def get_module_info(module_path: str) -> Dict:
    """Extract module information from folder name and structure."""
    module_name = os.path.basename(module_path)
    
    # Extract module number and title
    parts = module_name.split('_', 1)
    if len(parts) >= 2 and parts[0].isdigit():
        module_num = parts[0]
        title = ' '.join(word.capitalize() for word in parts[1].split('_'))
        return {
            'number': module_num,
            'title': title,
            'folder': module_name
        }
    else:
        return {
            'number': '00',
            'title': module_name.replace('_', ' ').title(),
            'folder': module_name
        }

def generate_learning_path():
    """Generate a learning path section for the README."""
    learning_content = [
        "## 🎯 Learning Path\n\n",
        "This repository is organized into progressive modules. Here's the recommended learning sequence:\n\n"
    ]
    
    modules = []
    modules_path = Path('src/modules')
    
    if modules_path.exists():
        for item in sorted(modules_path.iterdir()):
            if item.is_dir() and not item.name.startswith('__'):
                module_info = get_module_info(str(item))
                modules.append(module_info)
    
    for i, module in enumerate(modules, 1):
        learning_content.append(f"{i}. **Module {module['number']}: {module['title']}** (`src/modules/{module['folder']}/`)\n")
    
    learning_content.append("\n")
    return ''.join(learning_content)

def generate_module_documentation(module_path: str, module_info: Dict) -> str:
    """Generate documentation for a specific module."""
    content = [
        f"## Module {module_info['number']}: {module_info['title']}\n\n",
        f"📁 **Location**: `{module_path}/`\n\n"
    ]
    
    # Find README or description in module folder
    module_readme = os.path.join(module_path, 'README.md')
    if os.path.exists(module_readme):
        with open(module_readme, 'r', encoding='utf-8') as f:
            module_desc = f.read().strip()
            content.append(f"{module_desc}\n\n")
    
    # Analyze Python files in the module
    python_files = []
    for file in os.listdir(module_path):
        if file.endswith('.py') and file != '__init__.py':
            file_path = os.path.join(module_path, file)
            file_analysis = analyze_python_file(file_path)
            python_files.append((file, file_analysis))
    
    if python_files:
        content.append("### 📋 Files in this Module:\n\n")
        
        for filename, analysis in python_files:
            content.append(f"#### `{filename}`\n")
            
            # Module description
            if analysis['module_docstring']:
                content.append(f"{analysis['module_docstring']}\n\n")
            
            # Key classes
            if analysis['classes']:
                content.append("**Key Classes:**\n")
                for cls in analysis['classes']:
                    content.append(f"- `{cls['name']}`: {cls['docstring'].split('.')[0]}\n")
                content.append("\n")
            
            # Key functions
            if analysis['functions']:
                content.append("**Key Functions:**\n")
                for func in analysis['functions']:
                    desc = func['docstring'].split('.')[0] if func['docstring'] != 'No description available' else 'No description'
                    content.append(f"- `{func['name']}()`: {desc}\n")
                content.append("\n")
            
            content.append("---\n\n")
    
    return ''.join(content)

def update_readme():
    """Generate comprehensive README for LLM project."""
    readme_content = [
        "# 🤖 Build Large Language Model from Scratch\n\n",
        "A comprehensive implementation following the book's methodology, with clear chapter-by-chapter progression.\n\n",
        "[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)\n",
        "[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n",
        "[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n",
        "## 📚 About This Repository\n\n",
        "This repository contains a complete implementation of a Large Language Model (LLM) built from scratch, "
        "following best practices for educational purposes. Each chapter builds upon the previous one, "
        "creating a fully functional GPT-style model.\n\n"
    ]
    
    # Add learning path
    readme_content.append(generate_learning_path())
    
    # Quick start section
    readme_content.extend([
        "## 🚀 Quick Start\n\n",
        "```bash\n",
        "# Clone the repository\n",
        "git clone https://github.com/alizeeshan-07/Build_LLM_From_Scratch.git\n",
        "cd Build_LLM_From_Scratch\n\n",
        "# Create virtual environment\n",
        "python -m venv venv\n",
        "source venv/bin/activate  # On Windows: venv\\Scripts\\activate\n\n",
        "# Install dependencies\n",
        "pip install -r requirements.txt\n\n",
        "# Run a quick demo\n",
        "python examples/quick_start.py\n",
        "```\n\n"
    ])
    
    # Generate module-by-module documentation
    readme_content.append("## 📖 Module Details\n\n")
    
    modules_path = Path('src/modules')
    if modules_path.exists():
        modules = []
        for item in sorted(modules_path.iterdir()):
            if item.is_dir() and not item.name.startswith('__'):
                module_info = get_module_info(str(item))
                module_doc = generate_module_documentation(str(item), module_info)
                readme_content.append(module_doc)
    
    # Add utilities section
    utils_path = os.path.join('src', 'utils')
    if os.path.exists(utils_path):
        readme_content.append("## 🛠️ Utilities\n\n")
        readme_content.append("Common utilities used across all chapters:\n\n")
        
        for file in os.listdir(utils_path):
            if file.endswith('.py') and file != '__init__.py':
                file_path = os.path.join(utils_path, file)
                analysis = analyze_python_file(file_path)
                
                readme_content.append(f"### `{file}`\n")
                if analysis['module_docstring']:
                    readme_content.append(f"{analysis['module_docstring']}\n\n")
                
                if analysis['functions']:
                    for func in analysis['functions']:
                        desc = func['docstring'].split('.')[0]
                        readme_content.append(f"- `{func['name']}()`: {desc}\n")
                    readme_content.append("\n")
    
    # Footer
    readme_content.extend([
        "## 📄 Project Structure\n\n",
        "```\n",
        "src/\n",
        "├── modules/\n",
        "│   ├── 01_tokenization/           # Text tokenization methods\n",
        "│   ├── 02_embeddings/             # Word and positional embeddings\n",
        "│   ├── 03_attention/              # Attention mechanisms\n",
        "│   ├── 04_transformer_blocks/     # Transformer architecture\n",
        "│   ├── 05_gpt_model/              # Complete GPT model\n",
        "│   ├── 06_training/               # Training procedures\n",
        "│   ├── 07_inference/              # Text generation\n",
        "│   └── 08_fine_tuning/            # Model fine-tuning\n",
        "└── utils/                         # Common utilities\n",
        "```\n\n",
        "## 🤝 Contributing\n\n",
        "Contributions are welcome! Please feel free to submit a Pull Request. "
        "Make sure to follow the existing code structure and add appropriate documentation.\n\n",
        "## 📧 Contact\n\n",
        "Feel free to reach out if you have questions about the implementation or want to discuss LLM concepts!\n\n",
        "---\n",
        "*📝 This README is automatically updated when Python files are modified.*\n"
    ])
    
    # Write the README
    with open('README.md', 'w', encoding='utf-8') as f:
        f.writelines(readme_content)

if __name__ == "__main__":
    update_readme()
    print("✅ README.md updated successfully with LLM project structure!")