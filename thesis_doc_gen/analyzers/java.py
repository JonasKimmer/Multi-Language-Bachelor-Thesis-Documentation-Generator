"""Java code analyzer."""

import re
from pathlib import Path
from typing import Dict, List, Any
from .base import BaseAnalyzer


class JavaAnalyzer(BaseAnalyzer):
    """Analyzer for Java code."""

    def __init__(self):
        super().__init__("Java", [".java"])

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Analyze a Java file.

        Args:
            file_path: Path to the Java file

        Returns:
            Dictionary containing analysis results
        """
        result = {
            "path": str(file_path),
            "lines": 0,
            "classes": [],
            "interfaces": [],
            "methods": [],
            "imports": [],
            "package": None,
        }

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Count lines
            line_counts = self.count_lines(file_path)
            result["lines"] = line_counts["total"]

            # Extract structure
            result.update(self._extract_java_structure(content))

        except Exception as e:
            self.logger.error(f"Error analyzing {file_path}: {e}")

        return result

    def extract_structure(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract structural information from Java file.

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with structural information
        """
        return self.analyze_file(file_path)

    def _extract_java_structure(self, content: str) -> Dict[str, Any]:
        """Extract structural information from Java code."""
        result = {
            "classes": [],
            "interfaces": [],
            "methods": [],
            "imports": [],
            "package": None,
        }

        lines = content.split('\n')

        # Extract package
        package_pattern = re.compile(r'^\s*package\s+([\w.]+)\s*;')
        for line in lines:
            match = package_pattern.search(line)
            if match:
                result["package"] = match.group(1)
                break

        # Extract imports
        import_pattern = re.compile(r'^\s*import\s+(?:static\s+)?([\w.]+)(?:\.\*)?;')
        for line in lines:
            match = import_pattern.search(line)
            if match:
                result["imports"].append(match.group(1))

        # Extract classes
        class_pattern = re.compile(
            r'^\s*(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?(?:abstract\s+)?'
            r'class\s+(\w+)(?:\s+extends\s+([\w.]+))?(?:\s+implements\s+([\w\s,]+))?'
        )
        for i, line in enumerate(lines, 1):
            match = class_pattern.search(line)
            if match:
                class_info = {
                    "name": match.group(1),
                    "line": i,
                    "extends": match.group(2) if match.group(2) else None,
                    "implements": [s.strip() for s in match.group(3).split(',')] if match.group(3) else [],
                    "methods": [],
                }
                result["classes"].append(class_info)

        # Extract interfaces
        interface_pattern = re.compile(r'^\s*(?:public\s+)?interface\s+(\w+)(?:\s+extends\s+([\w\s,]+))?')
        for i, line in enumerate(lines, 1):
            match = interface_pattern.search(line)
            if match:
                interface_info = {
                    "name": match.group(1),
                    "line": i,
                    "extends": [s.strip() for s in match.group(2).split(',')] if match.group(2) else [],
                }
                result["interfaces"].append(interface_info)

        # Extract methods
        method_pattern = re.compile(
            r'^\s*(?:public|private|protected)\s+(?:static\s+)?(?:final\s+)?'
            r'(?:\w+(?:<[\w\s,]+>)?)\s+(\w+)\s*\(([^)]*)\)'
        )
        for i, line in enumerate(lines, 1):
            match = method_pattern.search(line)
            if match and not 'class ' in line and not 'interface ' in line:
                method_info = {
                    "name": match.group(1),
                    "line": i,
                    "parameters": match.group(2).strip() if match.group(2) else "",
                    "is_static": "static" in line,
                }
                result["methods"].append(method_info)

        return result

    def count_lines(self, file_path: Path) -> Dict[str, int]:
        """
        Count lines in a Java file.

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

            # Java comment detection
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
        Detect Java frameworks based on imports.

        Args:
            imports: List of import statements

        Returns:
            List of detected frameworks
        """
        frameworks = []
        framework_map = {
            "org.springframework": "Spring Framework",
            "javax.persistence": "JPA",
            "org.hibernate": "Hibernate",
            "org.junit": "JUnit",
            "org.testng": "TestNG",
            "javax.servlet": "Java Servlets",
            "org.apache.kafka": "Apache Kafka",
            "com.google.gson": "Gson",
            "com.fasterxml.jackson": "Jackson",
            "org.apache.commons": "Apache Commons",
        }

        for imp in imports:
            for key, framework in framework_map.items():
                if imp.startswith(key) and framework not in frameworks:
                    frameworks.append(framework)

        return frameworks
