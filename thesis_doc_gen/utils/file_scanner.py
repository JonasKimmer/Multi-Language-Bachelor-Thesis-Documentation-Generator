"""File system scanner for analyzing repository structure."""

import logging
from pathlib import Path
from typing import Dict, List, Any, Set
import mimetypes

logger = logging.getLogger(__name__)


class FileScanner:
    """Scans repository file structure."""

    # Default paths to exclude
    DEFAULT_EXCLUDE = [
        "node_modules/",
        "venv/",
        "env/",
        ".venv/",
        "__pycache__/",
        ".git/",
        "dist/",
        "build/",
        ".next/",
        ".cache/",
        "coverage/",
        ".pytest_cache/",
        "target/",
        "bin/",
        "obj/",
    ]

    def __init__(self, root_path: Path, exclude_paths: List[str] = None, max_file_size_kb: int = 500):
        """
        Initialize the file scanner.

        Args:
            root_path: Root directory to scan
            exclude_paths: List of paths to exclude
            max_file_size_kb: Maximum file size to analyze (in KB)
        """
        self.root_path = Path(root_path)
        self.exclude_paths = exclude_paths or self.DEFAULT_EXCLUDE
        self.max_file_size_bytes = max_file_size_kb * 1024
        self.logger = logging.getLogger(__name__)

    def scan(self) -> Dict[str, Any]:
        """
        Scan the repository structure.

        Returns:
            Dictionary with repository structure information
        """
        result = {
            "total_files": 0,
            "total_directories": 0,
            "total_size_bytes": 0,
            "files_by_extension": {},
            "directory_structure": {},
            "large_files": [],
        }

        try:
            all_files = []
            all_dirs = set()

            # Walk through directory
            for item in self.root_path.rglob("*"):
                # Check if should be excluded
                if self._should_exclude(item):
                    continue

                if item.is_file():
                    all_files.append(item)

                    # Track parent directories
                    parent = item.parent
                    while parent != self.root_path and parent not in all_dirs:
                        all_dirs.add(parent)
                        parent = parent.parent

            result["total_files"] = len(all_files)
            result["total_directories"] = len(all_dirs)

            # Analyze files
            for file_path in all_files:
                try:
                    file_size = file_path.stat().st_size
                    result["total_size_bytes"] += file_size

                    # Track by extension
                    ext = file_path.suffix.lower()
                    if ext:
                        if ext not in result["files_by_extension"]:
                            result["files_by_extension"][ext] = {
                                "count": 0,
                                "total_size": 0
                            }
                        result["files_by_extension"][ext]["count"] += 1
                        result["files_by_extension"][ext]["total_size"] += file_size

                    # Track large files
                    if file_size > self.max_file_size_bytes:
                        result["large_files"].append({
                            "path": str(file_path.relative_to(self.root_path)),
                            "size_kb": file_size / 1024
                        })

                except Exception as e:
                    self.logger.warning(f"Error analyzing {file_path}: {e}")

            # Build directory structure
            result["directory_structure"] = self._build_tree_structure()

        except Exception as e:
            self.logger.error(f"Error scanning repository: {e}")

        return result

    def _should_exclude(self, path: Path) -> bool:
        """
        Check if a path should be excluded.

        Args:
            path: Path to check

        Returns:
            True if path should be excluded
        """
        path_str = str(path.relative_to(self.root_path))

        for exclude_pattern in self.exclude_paths:
            if exclude_pattern in path_str:
                return True

        return False

    def _build_tree_structure(self) -> Dict[str, Any]:
        """
        Build a tree structure of the repository.

        Returns:
            Nested dictionary representing directory structure
        """
        tree = {}

        for item in self.root_path.rglob("*"):
            if self._should_exclude(item):
                continue

            if item.is_file():
                rel_path = item.relative_to(self.root_path)
                parts = rel_path.parts

                current = tree
                for i, part in enumerate(parts[:-1]):
                    if part not in current:
                        current[part] = {}
                    current = current[part]

                # Add file to current directory
                filename = parts[-1]
                if "__files__" not in current:
                    current["__files__"] = []
                current["__files__"].append(filename)

        return tree

    def get_project_type(self) -> List[str]:
        """
        Detect project type based on files.

        Returns:
            List of detected project types
        """
        project_types = []

        # Check for common project indicators
        indicators = {
            "Python": ["setup.py", "requirements.txt", "pyproject.toml", "Pipfile"],
            "Node.js": ["package.json", "package-lock.json", "yarn.lock"],
            "Java": ["pom.xml", "build.gradle", "build.gradle.kts"],
            "C#/.NET": ["*.csproj", "*.sln"],
            "Go": ["go.mod", "go.sum"],
            "Ruby": ["Gemfile", "Gemfile.lock"],
            "PHP": ["composer.json", "composer.lock"],
            "Rust": ["Cargo.toml", "Cargo.lock"],
            "Docker": ["Dockerfile", "docker-compose.yml"],
            "Web Frontend": ["index.html", "webpack.config.js", "vite.config.js"],
        }

        for project_type, files in indicators.items():
            for file_pattern in files:
                if "*" in file_pattern:
                    # Handle glob patterns
                    if list(self.root_path.glob(file_pattern)):
                        project_types.append(project_type)
                        break
                else:
                    # Handle exact filenames
                    if (self.root_path / file_pattern).exists():
                        project_types.append(project_type)
                        break

        return project_types

    def find_config_files(self) -> Dict[str, List[str]]:
        """
        Find configuration files in the repository.

        Returns:
            Dictionary mapping config types to file paths
        """
        config_files = {
            "build": [],
            "test": [],
            "lint": [],
            "ci_cd": [],
            "docker": [],
            "other": [],
        }

        config_patterns = {
            "build": ["package.json", "setup.py", "pom.xml", "build.gradle", "Cargo.toml", "go.mod"],
            "test": ["pytest.ini", "jest.config.js", "mocha.opts", "phpunit.xml"],
            "lint": [".eslintrc", ".pylintrc", ".editorconfig", "tslint.json"],
            "ci_cd": [".github/workflows", ".gitlab-ci.yml", "Jenkinsfile", ".travis.yml"],
            "docker": ["Dockerfile", "docker-compose.yml", ".dockerignore"],
        }

        for config_type, patterns in config_patterns.items():
            for pattern in patterns:
                # Check if it's a directory pattern
                if "/" in pattern:
                    matching = list(self.root_path.glob(pattern + "/*"))
                else:
                    matching = list(self.root_path.glob(pattern))

                for match in matching:
                    if not self._should_exclude(match):
                        rel_path = str(match.relative_to(self.root_path))
                        config_files[config_type].append(rel_path)

        return config_files

    def estimate_project_size(self) -> str:
        """
        Estimate project size category.

        Returns:
            Size category: "small", "medium", "large", "very_large"
        """
        scan_result = self.scan()
        total_files = scan_result["total_files"]

        if total_files < 20:
            return "small"
        elif total_files < 100:
            return "medium"
        elif total_files < 500:
            return "large"
        else:
            return "very_large"
