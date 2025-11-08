"""Factory for creating language-specific analyzers."""

from pathlib import Path
from typing import Dict, List, Optional
import logging

from .base import BaseAnalyzer, AnalysisResult
from .python import PythonAnalyzer
from .javascript import JavaScriptAnalyzer
from .java import JavaAnalyzer
from .sql import SQLAnalyzer

logger = logging.getLogger(__name__)


class AnalyzerFactory:
    """Factory for creating and managing language analyzers."""

    _analyzers = {
        "python": PythonAnalyzer,
        "javascript": JavaScriptAnalyzer,
        "java": JavaAnalyzer,
        "sql": SQLAnalyzer,
    }

    @classmethod
    def get_analyzer(cls, language: str) -> Optional[BaseAnalyzer]:
        """
        Get an analyzer for the specified language.

        Args:
            language: Programming language name (lowercase)

        Returns:
            Analyzer instance or None if not supported
        """
        language_lower = language.lower()
        analyzer_class = cls._analyzers.get(language_lower)
        if analyzer_class:
            return analyzer_class()
        return None

    @classmethod
    def get_all_analyzers(cls) -> Dict[str, BaseAnalyzer]:
        """
        Get all available analyzers.

        Returns:
            Dictionary mapping language names to analyzer instances
        """
        return {lang: analyzer() for lang, analyzer in cls._analyzers.items()}

    @classmethod
    def detect_languages(cls, directory: Path, exclude_paths: List[str] = None) -> List[str]:
        """
        Detect which programming languages are used in a directory.

        Args:
            directory: Directory to scan
            exclude_paths: List of paths to exclude

        Returns:
            List of detected language names
        """
        exclude_paths = exclude_paths or []
        detected_languages = []

        for lang_name, analyzer_class in cls._analyzers.items():
            analyzer = analyzer_class()

            # Check if any files with this language's extensions exist
            found_files = False
            for ext in analyzer.extensions:
                files = list(directory.rglob(f"*{ext}"))

                # Filter excluded paths
                filtered_files = []
                for file_path in files:
                    excluded = False
                    for exclude_pattern in exclude_paths:
                        if exclude_pattern in str(file_path):
                            excluded = True
                            break
                    if not excluded:
                        filtered_files.append(file_path)

                if filtered_files:
                    found_files = True
                    break

            if found_files:
                detected_languages.append(analyzer.language)

        logger.info(f"Detected languages: {detected_languages}")
        return detected_languages

    @classmethod
    def analyze_repository(
        cls,
        directory: Path,
        languages: Optional[List[str]] = None,
        exclude_paths: List[str] = None
    ) -> Dict[str, AnalysisResult]:
        """
        Analyze a repository for multiple languages.

        Args:
            directory: Root directory to analyze
            languages: List of languages to analyze (None for auto-detect)
            exclude_paths: List of paths to exclude

        Returns:
            Dictionary mapping language names to analysis results
        """
        exclude_paths = exclude_paths or []
        results = {}

        # Auto-detect languages if not specified
        if languages is None or (len(languages) == 1 and languages[0].lower() == "auto"):
            languages = cls.detect_languages(directory, exclude_paths)
            logger.info(f"Auto-detected languages: {languages}")

        # Analyze each language
        for language in languages:
            analyzer = cls.get_analyzer(language.lower())
            if analyzer:
                logger.info(f"Analyzing {language} files...")
                try:
                    result = analyzer.analyze_directory(directory, exclude_paths)
                    if result.files_analyzed:  # Only include if files were found
                        results[language] = result
                        logger.info(f"Analyzed {len(result.files_analyzed)} {language} files")
                except Exception as e:
                    logger.error(f"Error analyzing {language}: {e}")
            else:
                logger.warning(f"No analyzer available for language: {language}")

        return results

    @classmethod
    def supported_languages(cls) -> List[str]:
        """
        Get list of supported languages.

        Returns:
            List of supported language names
        """
        return [analyzer().language for analyzer in cls._analyzers.values()]
