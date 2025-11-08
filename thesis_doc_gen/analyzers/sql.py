"""SQL code analyzer."""

import re
from pathlib import Path
from typing import Dict, List, Any
from .base import BaseAnalyzer


class SQLAnalyzer(BaseAnalyzer):
    """Analyzer for SQL code."""

    def __init__(self):
        super().__init__("SQL", [".sql"])

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Analyze a SQL file.

        Args:
            file_path: Path to the SQL file

        Returns:
            Dictionary containing analysis results
        """
        result = {
            "path": str(file_path),
            "lines": 0,
            "tables": [],
            "views": [],
            "procedures": [],
            "functions": [],
            "indexes": [],
        }

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Count lines
            line_counts = self.count_lines(file_path)
            result["lines"] = line_counts["total"]

            # Extract structure
            result.update(self._extract_sql_structure(content))

        except Exception as e:
            self.logger.error(f"Error analyzing {file_path}: {e}")

        return result

    def extract_structure(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract structural information from SQL file.

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with structural information
        """
        return self.analyze_file(file_path)

    def _extract_sql_structure(self, content: str) -> Dict[str, Any]:
        """Extract structural information from SQL code."""
        result = {
            "tables": [],
            "views": [],
            "procedures": [],
            "functions": [],
            "indexes": [],
        }

        # Normalize SQL (case-insensitive)
        content_upper = content.upper()

        # Extract tables
        table_pattern = re.compile(
            r'CREATE\s+TABLE(?:\s+IF\s+NOT\s+EXISTS)?\s+([`"]?\w+[`"]?)',
            re.IGNORECASE
        )
        for match in table_pattern.finditer(content):
            table_name = match.group(1).strip('`"')
            if table_name not in result["tables"]:
                result["tables"].append(table_name)

        # Extract views
        view_pattern = re.compile(
            r'CREATE\s+(?:OR\s+REPLACE\s+)?VIEW\s+([`"]?\w+[`"]?)',
            re.IGNORECASE
        )
        for match in view_pattern.finditer(content):
            view_name = match.group(1).strip('`"')
            if view_name not in result["views"]:
                result["views"].append(view_name)

        # Extract stored procedures
        proc_pattern = re.compile(
            r'CREATE\s+(?:OR\s+REPLACE\s+)?PROCEDURE\s+([`"]?\w+[`"]?)',
            re.IGNORECASE
        )
        for match in proc_pattern.finditer(content):
            proc_name = match.group(1).strip('`"')
            if proc_name not in result["procedures"]:
                result["procedures"].append(proc_name)

        # Extract functions
        func_pattern = re.compile(
            r'CREATE\s+(?:OR\s+REPLACE\s+)?FUNCTION\s+([`"]?\w+[`"]?)',
            re.IGNORECASE
        )
        for match in func_pattern.finditer(content):
            func_name = match.group(1).strip('`"')
            if func_name not in result["functions"]:
                result["functions"].append(func_name)

        # Extract indexes
        index_pattern = re.compile(
            r'CREATE\s+(?:UNIQUE\s+)?INDEX\s+([`"]?\w+[`"]?)',
            re.IGNORECASE
        )
        for match in index_pattern.finditer(content):
            index_name = match.group(1).strip('`"')
            if index_name not in result["indexes"]:
                result["indexes"].append(index_name)

        return result

    def count_lines(self, file_path: Path) -> Dict[str, int]:
        """
        Count lines in a SQL file.

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

            # SQL comment detection
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
                elif stripped.startswith('--'):
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

    def detect_database_type(self, content: str) -> str:
        """
        Detect the type of SQL database based on content.

        Args:
            content: SQL file content

        Returns:
            Database type (MySQL, PostgreSQL, SQLite, etc.)
        """
        content_upper = content.upper()

        if 'AUTOINCREMENT' in content_upper or 'PRAGMA' in content_upper:
            return "SQLite"
        elif 'AUTO_INCREMENT' in content_upper or 'SHOW DATABASES' in content_upper:
            return "MySQL"
        elif 'SERIAL' in content_upper or 'RETURNING' in content_upper:
            return "PostgreSQL"
        elif 'IDENTITY' in content_upper or 'TOP ' in content_upper:
            return "SQL Server"
        else:
            return "Generic SQL"
