import os
import ast
import re

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
        # Match defaults with parameters (defaults apply to last N parameters)
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
        
        # Look for parameter descriptions (various formats)
        if line.lower().startswith('args:') or line.lower().startswith('parameters:'):
            current_section = 'params'
            continue
        elif line.lower().startswith('returns:') or line.lower().startswith('return:'):
            current_section = 'returns'
            continue
        elif line.lower().startswith('raises:') or line.lower().startswith('examples:'):
            current_section = 'other'
            continue
        
        # Parse parameter lines
        if current_section == 'params' and ':' in line:
            # Handle formats like "param_name (type): description" or "param_name: description"
            param_match = re.match(r'^\s*(\w+)(?:\s*\([^)]+\))?\s*:\s*(.+)', line)
            if param_match:
                param_name, description = param_match.groups()
                param_descriptions[param_name] = description.strip()
        
        # Parse return description
        elif current_section == 'returns' and line:
            if not return_description:
                return_description = line
            else:
                return_description += ' ' + line
    
    return param_descriptions, return_description

def extract_docstring_and_functions(file_path):
    """Extract module docstring and detailed function information from a Python file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            content = file.read()
            tree = ast.parse(content)
        except SyntaxError:
            return None, []
    
    # Get module docstring
    module_docstring = ast.get_docstring(tree)
    
    # Get function definitions with detailed info
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_info = extract_function_info(node)
            
            # Parse docstring for parameter and return descriptions
            param_descriptions, return_description = parse_docstring_sections(func_info['docstring'])
            func_info['param_descriptions'] = param_descriptions
            func_info['return_description'] = return_description
            
            functions.append(func_info)
    
    return module_docstring, functions

def format_function_signature(func_info):
    """Create a readable function signature."""
    params = []
    for param in func_info['parameters']:
        param_str = f"{param['name']}: {param['type']}"
        if param['default'] is not None:
            param_str += f" = {param['default']}"
        params.append(param_str)
    
    params_str = ', '.join(params)
    return f"{func_info['name']}({params_str}) -> {func_info['return_type']}"

def update_readme():
    """Update README.md with detailed summaries of all Python files."""
    readme_content = [
        "# Project Name\n\n",
        "## Overview\n",
        "This project contains Python modules with automatically generated documentation.\n\n",
        "## File Summaries\n\n"
    ]
    
    for root, dirs, files in os.walk('src'):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                file_path = os.path.join(root, file)
                module_doc, functions = extract_docstring_and_functions(file_path)
                
                readme_content.append(f"### 📄 {file}\n")
                
                # Module description
                if module_doc:
                    readme_content.append(f"{module_doc}\n\n")
                else:
                    readme_content.append("*No module description available.*\n\n")
                
                # Functions
                if functions:
                    readme_content.append("#### Functions:\n\n")
                    
                    for func in functions:
                        # Function signature
                        signature = format_function_signature(func)
                        readme_content.append(f"**`{signature}`**\n\n")
                        
                        # Function description
                        main_desc = func['docstring'].split('\n')[0] if func['docstring'] != 'No description available' else func['docstring']
                        readme_content.append(f"{main_desc}\n\n")
                        
                        # Parameters
                        if func['parameters']:
                            readme_content.append("*Parameters:*\n")
                            for param in func['parameters']:
                                param_desc = func['param_descriptions'].get(param['name'], 'No description')
                                default_info = f" (default: {param['default']})" if param['default'] is not None else ""
                                readme_content.append(f"- **{param['name']}** (`{param['type']}`{default_info}): {param_desc}\n")
                            readme_content.append("\n")
                        
                        # Return information
                        return_desc = func['return_description'] or "No return description"
                        readme_content.append(f"*Returns:* `{func['return_type']}` - {return_desc}\n\n")
                        
                        readme_content.append("---\n\n")
                else:
                    readme_content.append("*No functions found in this module.*\n\n")
    
    # Add footer
    readme_content.extend([
        "## Notes\n\n",
        "- This documentation is automatically generated from Python docstrings\n",
        "- Function signatures include type hints when available\n",
        "- Parameter and return descriptions are extracted from docstrings\n"
    ])
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.writelines(readme_content)

if __name__ == "__main__":
    update_readme()
    print("README.md updated successfully with detailed function information!")