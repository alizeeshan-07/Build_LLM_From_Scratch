import os
import ast
import re

def extract_docstring_and_functions(file_path):
    """Extract module docstring and function definitions from a Python file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            tree = ast.parse(file.read())
        except SyntaxError:
            return None, []
    
    # Get module docstring
    module_docstring = ast.get_docstring(tree)
    
    # Get function definitions
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_docstring = ast.get_docstring(node)
            functions.append({
                'name': node.name,
                'docstring': func_docstring or 'No description available'
            })
    
    return module_docstring, functions

def update_readme():
    """Update README.md with summaries of all Python files."""
    readme_content = ["# Project Name\n\n", "## File Summaries\n\n"]
    
    for root, dirs, files in os.walk('src'):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                file_path = os.path.join(root, file)
                module_doc, functions = extract_docstring_and_functions(file_path)
                
                readme_content.append(f"### {file}\n")
                
                if module_doc:
                    readme_content.append(f"{module_doc}\n\n")
                else:
                    readme_content.append("No module description available.\n\n")
                
                if functions:
                    readme_content.append("**Functions:**\n")
                    for func in functions:
                        readme_content.append(f"- `{func['name']}()`: {func['docstring']}\n")
                    readme_content.append("\n")
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.writelines(readme_content)

if __name__ == "__main__":
    update_readme()
    print("README.md updated successfully!")