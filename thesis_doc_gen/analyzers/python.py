"""Python-specific code analyzer."""

import ast
import re
from pathlib import Path
from typing import Dict, List, Any
from .base import BaseAnalyzer


class PythonAnalyzer(BaseAnalyzer):
    """Analyzer for Python code."""

    def __init__(self):
        super().__init__("Python", [".py", ".pyw"])

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Analyze a Python file.

        Args:
            file_path: Path to the Python file

        Returns:
            Dictionary containing analysis results
        """
        result = {
            "path": str(file_path),
            "lines": 0,
            "classes": [],
            "functions": [],
            "imports": [],
            "docstrings": [],
        }

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Count lines
            line_counts = self.count_lines(file_path)
            result["lines"] = line_counts["total"]

            # Parse AST
            try:
                tree = ast.parse(content, filename=str(file_path))
                result.update(self._analyze_ast(tree))
            except SyntaxError as e:
                self.logger.warning(f"Syntax error in {file_path}: {e}")

        except Exception as e:
            self.logger.error(f"Error analyzing {file_path}: {e}")

        return result

    def extract_structure(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract structural information from Python file.

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with structural information
        """
        return self.analyze_file(file_path)

    def _analyze_ast(self, tree: ast.AST) -> Dict[str, Any]:
        """Analyze the AST of a Python file."""
        result = {
            "classes": [],
            "functions": [],
            "imports": [],
            "docstrings": [],
        }

        for node in ast.walk(tree):
            # Extract classes
            if isinstance(node, ast.ClassDef):
                class_info = {
                    "name": node.name,
                    "line": node.lineno,
                    "methods": [],
                    "bases": [self._get_name(base) for base in node.bases],
                    "docstring": ast.get_docstring(node),
                }

                # Extract methods
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        class_info["methods"].append({
                            "name": item.name,
                            "line": item.lineno,
                            "args": [arg.arg for arg in item.args.args],
                            "docstring": ast.get_docstring(item),
                            "is_private": item.name.startswith("_"),
                            "is_property": any(
                                isinstance(d, ast.Name) and d.id == "property"
                                for d in item.decorator_list
                            ),
                        })

                result["classes"].append(class_info)

            # Extract top-level functions
            elif isinstance(node, ast.FunctionDef):
                # Check if it's a top-level function (not a method)
                parent = getattr(node, 'parent', None)
                if not isinstance(parent, ast.ClassDef):
                    func_info = {
                        "name": node.name,
                        "line": node.lineno,
                        "args": [arg.arg for arg in node.args.args],
                        "docstring": ast.get_docstring(node),
                        "is_async": isinstance(node, ast.AsyncFunctionDef),
                        "decorators": [self._get_name(d) for d in node.decorator_list],
                    }
                    result["functions"].append(func_info)

            # Extract imports
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    result["imports"].append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    result["imports"].append(node.module)

        # Extract docstrings
        module_docstring = ast.get_docstring(tree)
        if module_docstring:
            result["docstrings"].append(module_docstring)

        return result

    def _get_name(self, node: ast.AST) -> str:
        """Get the name from an AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Call):
            return self._get_name(node.func)
        return str(node)

    def count_lines(self, file_path: Path) -> Dict[str, int]:
        """
        Count lines in a Python file.

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with line counts
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            total = len(lines)
            blank = sum(1 for line in lines if not line.strip())

            # Python comment detection
            comments = 0
            in_multiline_string = False
            for line in lines:
                stripped = line.strip()

                # Check for multiline strings (docstrings)
                if '"""' in stripped or "'''" in stripped:
                    in_multiline_string = not in_multiline_string

                # Single-line comments
                if stripped.startswith('#'):
                    comments += 1
                elif in_multiline_string:
                    comments += 1

            code = total - blank - comments

            return {
                "total": total,
                "code": code,
                "comments": comments,
                "blank": blank
            }
        except Exception as e:
            self.logger.warning(f"Error counting lines in {file_path}: {e}")
            return {"total": 0, "code": 0, "comments": 0, "blank": 0}

    def detect_frameworks(self, imports: List[str]) -> List[str]:
        """
        Detect Python frameworks based on imports.

        Args:
            imports: List of import statements

        Returns:
            List of detected frameworks
        """
        frameworks = []
        framework_map = {
            "django": "Django",
            "flask": "Flask",
            "fastapi": "FastAPI",
            "tornado": "Tornado",
            "pytest": "pytest",
            "unittest": "unittest",
            "pandas": "Pandas",
            "numpy": "NumPy",
            "tensorflow": "TensorFlow",
            "torch": "PyTorch",
            "sklearn": "scikit-learn",
            "requests": "Requests",
            "sqlalchemy": "SQLAlchemy",
            "asyncio": "asyncio",
        }

        for imp in imports:
            for key, framework in framework_map.items():
                if imp.startswith(key) and framework not in frameworks:
                    frameworks.append(framework)

        return frameworks
