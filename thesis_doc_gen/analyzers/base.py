"""Base analyzer class for language-specific code analysis."""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class AnalysisResult:
    """Container for analysis results."""

    def __init__(self):
        self.language: str = ""
        self.files_analyzed: List[Path] = []
        self.total_lines: int = 0
        self.classes: List[Dict[str, Any]] = []
        self.functions: List[Dict[str, Any]] = []
        self.imports: List[str] = []
        self.dependencies: List[str] = []
        self.frameworks: List[str] = []
        self.complexity_metrics: Dict[str, Any] = {}
        self.design_patterns: List[str] = []
        self.comments_ratio: float = 0.0
        self.test_coverage_estimate: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "language": self.language,
            "files_analyzed": [str(f) for f in self.files_analyzed],
            "total_lines": self.total_lines,
            "classes": self.classes,
            "functions": self.functions,
            "imports": self.imports,
            "dependencies": self.dependencies,
            "frameworks": self.frameworks,
            "complexity_metrics": self.complexity_metrics,
            "design_patterns": self.design_patterns,
            "comments_ratio": self.comments_ratio,
            "test_coverage_estimate": self.test_coverage_estimate,
        }


class BaseAnalyzer(ABC):
    """Abstract base class for language-specific analyzers."""

    def __init__(self, language: str, extensions: List[str]):
        """
        Initialize the analyzer.

        Args:
            language: Programming language name
            extensions: List of file extensions (e.g., ['.py', '.pyw'])
        """
        self.language = language
        self.extensions = extensions
        self.logger = logging.getLogger(f"{__name__}.{language}")

    @abstractmethod
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Analyze a single file.

        Args:
            file_path: Path to the file to analyze

        Returns:
            Dictionary containing analysis results for the file
        """
        pass

    @abstractmethod
    def extract_structure(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract structural information (classes, functions, etc.).

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with structural information
        """
        pass

    def analyze_directory(self, directory: Path, exclude_paths: List[str] = None) -> AnalysisResult:
        """
        Analyze all files of this language in a directory.

        Args:
            directory: Root directory to analyze
            exclude_paths: List of paths to exclude

        Returns:
            AnalysisResult containing aggregated results
        """
        exclude_paths = exclude_paths or []
        result = AnalysisResult()
        result.language = self.language

        # Find all matching files
        matching_files = []
        for ext in self.extensions:
            matching_files.extend(directory.rglob(f"*{ext}"))

        # Filter excluded paths
        filtered_files = []
        for file_path in matching_files:
            excluded = False
            for exclude_pattern in exclude_paths:
                if exclude_pattern in str(file_path):
                    excluded = True
                    break
            if not excluded:
                filtered_files.append(file_path)

        self.logger.info(f"Found {len(filtered_files)} {self.language} files")

        # Analyze each file
        for file_path in filtered_files:
            try:
                file_result = self.analyze_file(file_path)
                result.files_analyzed.append(file_path)
                result.total_lines += file_result.get("lines", 0)

                # Aggregate classes and functions
                if "classes" in file_result:
                    result.classes.extend(file_result["classes"])
                if "functions" in file_result:
                    result.functions.extend(file_result["functions"])
                if "imports" in file_result:
                    result.imports.extend(file_result["imports"])

            except Exception as e:
                self.logger.warning(f"Error analyzing {file_path}: {e}")

        # Calculate aggregate metrics
        if result.files_analyzed:
            result.dependencies = list(set(result.imports))
            result.comments_ratio = self._calculate_comments_ratio(result)

            # Detect frameworks (if analyzer implements it)
            if hasattr(self, 'detect_frameworks'):
                result.frameworks = self.detect_frameworks(result.imports)

        return result

    def _calculate_comments_ratio(self, result: AnalysisResult) -> float:
        """Calculate the ratio of comments to code."""
        # Default implementation - can be overridden
        return 0.0

    def is_test_file(self, file_path: Path) -> bool:
        """
        Check if a file is a test file.

        Args:
            file_path: Path to check

        Returns:
            True if the file is a test file
        """
        test_indicators = ['test_', '_test', 'tests/', 'test.', '.test.', 'spec.', '.spec.']
        file_str = str(file_path).lower()
        return any(indicator in file_str for indicator in test_indicators)

    def count_lines(self, file_path: Path) -> Dict[str, int]:
        """
        Count lines in a file (total, code, comments, blank).

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

            # Simple comment detection (language-specific analyzers should override)
            comments = 0
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('#') or stripped.startswith('//'):
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
