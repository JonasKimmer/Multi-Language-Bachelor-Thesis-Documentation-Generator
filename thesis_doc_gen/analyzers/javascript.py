"""JavaScript/TypeScript code analyzer."""

import re
from pathlib import Path
from typing import Dict, List, Any
from .base import BaseAnalyzer


class JavaScriptAnalyzer(BaseAnalyzer):
    """Analyzer for JavaScript and TypeScript code."""

    def __init__(self):
        super().__init__("JavaScript/TypeScript", [".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"])

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Analyze a JavaScript/TypeScript file.

        Args:
            file_path: Path to the file

        Returns:
            Dictionary containing analysis results
        """
        result = {
            "path": str(file_path),
            "lines": 0,
            "classes": [],
            "functions": [],
            "imports": [],
            "exports": [],
            "is_typescript": file_path.suffix in [".ts", ".tsx"],
        }

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Count lines
            line_counts = self.count_lines(file_path)
            result["lines"] = line_counts["total"]

            # Extract structure
            result.update(self._extract_js_structure(content))

        except Exception as e:
            self.logger.error(f"Error analyzing {file_path}: {e}")

        return result

    def extract_structure(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract structural information from JS/TS file.

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with structural information
        """
        return self.analyze_file(file_path)

    def _extract_js_structure(self, content: str) -> Dict[str, Any]:
        """Extract structural information from JavaScript/TypeScript code."""
        result = {
            "classes": [],
            "functions": [],
            "imports": [],
            "exports": [],
        }

        lines = content.split('\n')

        # Extract classes
        class_pattern = re.compile(r'^\s*(?:export\s+)?(?:default\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?')
        for i, line in enumerate(lines, 1):
            match = class_pattern.search(line)
            if match:
                class_info = {
                    "name": match.group(1),
                    "line": i,
                    "extends": match.group(2) if match.group(2) else None,
                    "methods": [],
                }
                result["classes"].append(class_info)

        # Extract functions
        func_patterns = [
            re.compile(r'^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)'),  # function declarations
            re.compile(r'^\s*(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:\([^)]*\)|[^=]+)\s*=>'),  # arrow functions
        ]

        for i, line in enumerate(lines, 1):
            for pattern in func_patterns:
                match = pattern.search(line)
                if match:
                    func_info = {
                        "name": match.group(1),
                        "line": i,
                        "is_async": "async" in line,
                        "is_arrow": "=>" in line,
                    }
                    result["functions"].append(func_info)
                    break

        # Extract imports
        import_patterns = [
            re.compile(r'^\s*import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]'),  # import ... from '...'
            re.compile(r'^\s*import\s+[\'"]([^\'"]+)[\'"]'),  # import '...'
            re.compile(r'^\s*require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)'),  # require('...')
        ]

        for line in lines:
            for pattern in import_patterns:
                match = pattern.search(line)
                if match:
                    result["imports"].append(match.group(1))
                    break

        # Extract exports
        export_patterns = [
            re.compile(r'^\s*export\s+default\s+(\w+)'),
            re.compile(r'^\s*export\s+\{([^}]+)\}'),
            re.compile(r'^\s*module\.exports\s*='),
        ]

        for line in lines:
            for pattern in export_patterns:
                match = pattern.search(line)
                if match:
                    export_name = match.group(1) if match.lastindex else "default"
                    result["exports"].append(export_name)
                    break

        return result

    def count_lines(self, file_path: Path) -> Dict[str, int]:
        """
        Count lines in a JavaScript/TypeScript file.

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

            # JavaScript/TypeScript comment detection
            comments = 0
            in_multiline_comment = False

            for line in lines:
                stripped = line.strip()

                # Check for multiline comments
                if '/*' in stripped:
                    in_multiline_comment = True
                if '*/' in stripped:
                    in_multiline_comment = False
                    comments += 1
                    continue

                if in_multiline_comment:
                    comments += 1
                elif stripped.startswith('//'):
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
        Detect JavaScript/TypeScript frameworks based on imports.

        Args:
            imports: List of import statements

        Returns:
            List of detected frameworks
        """
        frameworks = []
        framework_map = {
            "react": "React",
            "vue": "Vue.js",
            "angular": "Angular",
            "express": "Express.js",
            "next": "Next.js",
            "nuxt": "Nuxt.js",
            "svelte": "Svelte",
            "axios": "Axios",
            "lodash": "Lodash",
            "moment": "Moment.js",
            "jquery": "jQuery",
            "webpack": "Webpack",
            "babel": "Babel",
            "typescript": "TypeScript",
            "jest": "Jest",
            "mocha": "Mocha",
            "cypress": "Cypress",
        }

        for imp in imports:
            for key, framework in framework_map.items():
                if key in imp.lower() and framework not in frameworks:
                    frameworks.append(framework)

        return frameworks
