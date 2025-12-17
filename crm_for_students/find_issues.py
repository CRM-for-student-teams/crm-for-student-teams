import ast
import os
import sys
from typing import List, Dict, Any

def analyze_file(filepath: str) -> List[str]:
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        tree = ast.parse(content)
    except Exception as e:
        return [f"Error parsing {filepath}: {e}"]

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if not ast.get_docstring(node):
                issues.append(f"{filepath}:{node.lineno} - Missing docstring for class '{node.name}'")
        
        elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            if not ast.get_docstring(node):
                issues.append(f"{filepath}:{node.lineno} - Missing docstring for function/method '{node.name}'")
            
            # Check return type annotation
            if node.returns is None:
                 # __init__ usually doesn't need return annotation, but strict typing might require -> None
                if node.name != "__init__":
                    issues.append(f"{filepath}:{node.lineno} - Missing return type hint for '{node.name}'")

            # Check argument type annotations
            for arg in node.args.args:
                if arg.arg in ('self', 'cls'):
                    continue
                if arg.annotation is None:
                    issues.append(f"{filepath}:{node.lineno} - Missing type hint for argument '{arg.arg}' in '{node.name}'")
            
            # Check keyword-only argument type annotations
            for arg in node.args.kwonlyargs:
                if arg.annotation is None:
                     issues.append(f"{filepath}:{node.lineno} - Missing type hint for kw-argument '{arg.arg}' in '{node.name}'")

    return issues

def main():
    target_dir = os.path.join(os.getcwd(), 'apps')
    if not os.path.exists(target_dir):
        print(f"Directory {target_dir} not found.")
        return

    all_issues = []
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                all_issues.extend(analyze_file(filepath))

    if all_issues:
        print("Found the following issues:")
        for issue in sorted(all_issues):
            print(issue)
        print(f"\nTotal issues found: {len(all_issues)}")
    else:
        print("No missing docstrings or type hints found!")

if __name__ == "__main__":
    main()
