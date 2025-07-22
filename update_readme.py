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
    if os.path.exists(module_path):
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
    else:
        content.append("*Module files will appear here as you implement them.*\n\n")
    
    return ''.join(content)

def add_documentation_links():
    """Add links to documentation files."""
    content = [
        "## 📚 Documentation & Learning Resources\n\n",
        "This repository includes comprehensive documentation to support your learning journey:\n\n",
        "### 📖 **Core Documentation**\n",
        "- **[🎯 Learning Path](docs/learning_path.md)** - Step-by-step guide through all modules with time estimates, prerequisites, and study tips\n",
        "- **[📚 Resources](docs/resources.md)** - Curated collection of papers, books, videos, and online resources\n", 
        "- **[🔧 Troubleshooting](docs/troubleshooting.md)** - Solutions to common implementation, training, and setup issues\n\n",
        "### 🎯 **Module-Specific Guides**\n",
        "Each module includes its own README with:\n",
        "- Learning objectives and key concepts\n",
        "- Implementation details and explanations\n",
        "- Usage examples and best practices\n",
        "- Common issues and debugging tips\n\n"
    ]
    return ''.join(content)

def update_readme():
    """Generate comprehensive README for LLM project."""
    readme_content = [
        "# 🤖 Build Large Language Model from Scratch\n\n",
        "A comprehensive implementation following a modular, educational approach to understanding and building Large Language Models (LLMs) from the ground up.\n\n",
        "[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)\n",
        "[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)\n",
        "[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n",
        "[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n",
        "[![Auto-Update Docs](https://img.shields.io/badge/docs-auto--updated-green.svg)](.github/workflows/update-readme.yml)\n\n",
        "## 🎯 About This Project\n\n",
        "This repository provides a **complete, educational implementation** of Large Language Models, designed for:\n\n",
        "- 🎓 **Students and researchers** learning about transformer architectures\n",
        "- 💻 **Developers** wanting to understand LLMs from first principles  \n",
        "- 🔬 **Practitioners** looking for clean, well-documented reference implementations\n",
        "- 🤝 **Contributors** interested in advancing open-source ML education\n\n",
        "### ✨ **Key Features**\n",
        "- **Progressive complexity**: Each module builds naturally on previous concepts\n",
        "- **Production-quality code**: Clean, typed, tested, and documented\n",
        "- **Educational focus**: Extensive explanations, visualizations, and examples\n",
        "- **Auto-updating documentation**: README stays synchronized with code changes\n",
        "- **Interactive learning**: Jupyter notebooks for experimentation\n",
        "- **Comprehensive testing**: Unit tests ensure code correctness\n\n"
    ]
    
    # Add documentation links
    readme_content.append(add_documentation_links())
    
    # Add learning path
    readme_content.append(generate_learning_path())
    
    # Quick start section
    readme_content.extend([
        "## 🚀 Quick Start\n\n",
        "### **Prerequisites**\n",
        "- Python 3.8+ installed\n",
        "- Basic familiarity with PyTorch and neural networks\n",
        "- 8GB+ RAM recommended (16GB+ for larger experiments)\n\n",
        "### **Installation**\n",
        "```bash\n",
        "# Clone the repository\n",
        "git clone https://github.com/alizeeshan-07/Build_LLM_From_Scratch.git\n",
        "cd Build_LLM_From_Scratch\n\n",
        "# Create and activate virtual environment\n",
        "python -m venv venv\n",
        "source venv/bin/activate  # On Windows: venv\\Scripts\\activate\n\n",
        "# Install the project in development mode\n",
        "pip install -e .\n\n",
        "# Verify installation\n",
        "python examples/quick_start.py\n",
        "```\n\n",
        "### **First Steps**\n",
        "1. 📖 **Read the [Learning Path](docs/learning_path.md)** to understand the progression\n",
        "2. 🏃‍♂️ **Start with Module 1**: `src/modules/01_tokenization/`\n",
        "3. 📚 **Follow along** with the module README and examples\n",
        "4. 🧪 **Experiment** with the Jupyter notebooks in `notebooks/`\n",
        "5. ❓ **Get help** from our [Troubleshooting Guide](docs/troubleshooting.md)\n\n"
    ])
    
    # Generate module-by-module documentation
    readme_content.append("## 📖 Module Overview\n\n")
    
    modules_path = Path('src/modules')
    if modules_path.exists():
        for item in sorted(modules_path.iterdir()):
            if item.is_dir() and not item.name.startswith('__'):
                module_info = get_module_info(str(item))
                module_doc = generate_module_documentation(str(item), module_info)
                readme_content.append(module_doc)
    else:
        readme_content.append("*Modules will appear here as you implement them. Start by creating the first module!*\n\n")
    
    # Add utilities section
    utils_path = os.path.join('src', 'utils')
    if os.path.exists(utils_path):
        readme_content.append("## 🛠️ Utilities & Tools\n\n")
        readme_content.append("Common utilities and tools used across all modules:\n\n")
        
        for file in sorted(os.listdir(utils_path)):
            if file.endswith('.py') and file != '__init__.py':
                file_path = os.path.join(utils_path, file)
                analysis = analyze_python_file(file_path)
                
                readme_content.append(f"### `{file}`\n")
                if analysis['module_docstring']:
                    readme_content.append(f"{analysis['module_docstring']}\n\n")
                
                if analysis['functions']:
                    readme_content.append("**Key Functions:**\n")
                    for func in analysis['functions']:
                        desc = func['docstring'].split('.')[0] if func['docstring'] != 'No description available' else 'No description'
                        readme_content.append(f"- `{func['name']}()`: {desc}\n")
                    readme_content.append("\n")
    
    # Project structure
    readme_content.extend([
        "## 📁 Project Structure\n\n",
        "```\n",
        "Build_LLM_From_Scratch/\n",
        "├── 📁 src/\n",
        "│   ├── 📁 modules/                    # Core LLM implementation modules\n",
        "│   │   ├── 📁 01_tokenization/        # Text tokenization methods\n",
        "│   │   ├── 📁 02_embeddings/          # Word and positional embeddings\n",
        "│   │   ├── 📁 03_attention/           # Attention mechanisms\n",
        "│   │   ├── 📁 04_transformer_blocks/  # Transformer architecture\n",
        "│   │   ├── 📁 05_gpt_model/           # Complete GPT model\n",
        "│   │   ├── 📁 06_training/            # Training procedures\n",
        "│   │   ├── 📁 07_inference/           # Text generation\n",
        "│   │   └── 📁 08_fine_tuning/         # Model fine-tuning\n",
        "│   └── 📁 utils/                      # Common utilities\n",
        "├── 📁 examples/                       # Usage examples and demos\n",
        "├── 📁 notebooks/                      # Interactive Jupyter notebooks\n",
        "├── 📁 tests/                          # Unit tests\n",
        "├── 📁 docs/                           # Comprehensive documentation\n",
        "└── 📁 data/                           # Sample datasets (git-ignored)\n",
        "```\n\n"
    ])
    
    # Usage examples
    readme_content.extend([
        "## 💡 Usage Examples\n\n",
        "### **Command Line Interface**\n",
        "```bash\n",
        "# Quick start demo\n",
        "python examples/quick_start.py\n\n",
        "# Train a small model\n",
        "python examples/train_small_model.py\n\n",
        "# Generate text\n",
        "python examples/generate_text.py --prompt \"The future of AI is\"\n\n",
        "# Use the CLI tool\n",
        "build-llm train --config configs/small_model.yaml\n",
        "build-llm generate --prompt \"Hello, world!\" --max-length 50\n",
        "```\n\n",
        "### **Python API**\n",
        "```python\n",
        "from src.modules.tokenization import SimpleTokenizer\n",
        "from src.modules.gpt_model import GPTModel\n",
        "from src.utils import plot_attention_weights\n\n",
        "# Tokenize text\n",
        "tokenizer = SimpleTokenizer()\n",
        "tokens = tokenizer.encode(\"Hello, world!\")\n\n",
        "# Create and use model\n",
        "model = GPTModel(vocab_size=10000, d_model=512)\n",
        "output = model(tokens)\n\n",
        "# Visualize attention\n",
        "plot_attention_weights(attention_weights, tokens)\n",
        "```\n\n"
    ])
    
    # Contributing section
    readme_content.extend([
        "## 🤝 Contributing\n\n",
        "We welcome contributions! This project is designed to be educational and collaborative.\n\n",
        "### **Ways to Contribute**\n",
        "- 🐛 **Bug reports** - Found an issue? Let us know!\n",
        "- 💡 **Feature requests** - Ideas for improvements?\n",
        "- 📝 **Documentation** - Help make explanations clearer\n",
        "- 🧪 **Testing** - Add tests for better reliability\n",
        "- 🎓 **Educational content** - Notebooks, examples, tutorials\n",
        "- 🔧 **Code improvements** - Optimizations and clean-ups\n\n",
        "### **Getting Started with Contributing**\n",
        "1. Read our [Contributing Guidelines](CONTRIBUTING.md)\n",
        "2. Check out [Good First Issues](https://github.com/alizeeshan-07/Build_LLM_From_Scratch/labels/good%20first%20issue)\n",
        "3. Fork the repository and create a feature branch\n",
        "4. Make your changes and add tests if applicable\n",
        "5. Submit a pull request with a clear description\n\n",
        "See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.\n\n"
    ])
    
    # Footer
    readme_content.extend([
        "## 📊 Project Stats\n\n",
        "- 🐍 **Language**: Python 3.8+\n",
        "- 🔥 **Framework**: PyTorch 2.0+\n",
        "- 📦 **Modules**: 8 core learning modules\n",
        "- 🧪 **Tests**: Comprehensive test coverage\n",
        "- 📚 **Documentation**: Auto-generated and maintained\n",
        "- 🤖 **CI/CD**: Automated testing and documentation updates\n\n",
        "## 🙏 Acknowledgments\n\n",
        "This project is inspired by:\n",
        "- 📖 \"Build a Large Language Model (From Scratch)\" book\n",
        "- 🎓 Stanford CS224N course materials\n",
        "- 💻 Andrej Karpathy's educational content\n",
        "- 🤗 Hugging Face's transformer implementations\n",
        "- 🌟 The broader open-source ML community\n\n",
        "## 📄 License\n\n",
        "This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.\n\n",
        "## 📞 Support & Contact\n\n",
        "- 💬 **Discussions**: [GitHub Discussions](https://github.com/alizeeshan-07/Build_LLM_From_Scratch/discussions)\n",
        "- 🐛 **Issues**: [GitHub Issues](https://github.com/alizeeshan-07/Build_LLM_From_Scratch/issues)\n",
        "- 📧 **Email**: Open an issue for questions\n",
        "- 📚 **Documentation**: Check our [docs folder](docs/) for detailed guides\n\n",
        "---\n\n",
        "**⭐ Star this repository if it helps you learn!**\n\n",
        "*📝 This README is automatically updated when Python files are modified. Last updated: Auto-generated by GitHub Actions.*\n"
    ])
    
    # Write the README
    with open('README.md', 'w', encoding='utf-8') as f:
        f.writelines(readme_content)

if __name__ == "__main__":
    update_readme()
    print("✅ README.md updated successfully with comprehensive LLM project documentation!")