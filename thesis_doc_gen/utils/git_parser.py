"""Git repository history parser."""

import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import subprocess

logger = logging.getLogger(__name__)


class GitCommit:
    """Represents a Git commit."""

    def __init__(self, hash: str, author: str, date: datetime, message: str, files: List[str]):
        self.hash = hash
        self.author = author
        self.date = date
        self.message = message
        self.files = files

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "hash": self.hash,
            "author": self.author,
            "date": self.date.isoformat(),
            "message": self.message,
            "files": self.files,
        }


class GitParser:
    """Parser for Git repository history."""

    def __init__(self, repo_path: Path):
        """
        Initialize the Git parser.

        Args:
            repo_path: Path to the Git repository
        """
        self.repo_path = Path(repo_path)
        self.logger = logging.getLogger(__name__)

    def is_git_repo(self) -> bool:
        """
        Check if the path is a Git repository.

        Returns:
            True if it's a Git repository
        """
        git_dir = self.repo_path / ".git"
        return git_dir.exists()

    def get_commits(self, limit: Optional[int] = None) -> List[GitCommit]:
        """
        Get commit history.

        Args:
            limit: Maximum number of commits to retrieve (None for all)

        Returns:
            List of GitCommit objects
        """
        if not self.is_git_repo():
            self.logger.warning(f"{self.repo_path} is not a Git repository")
            return []

        try:
            # Format: hash|author|date|message
            cmd = [
                "git",
                "-C", str(self.repo_path),
                "log",
                "--pretty=format:%H|%an|%ai|%s",
                "--name-only"
            ]

            if limit:
                cmd.append(f"-{limit}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )

            commits = []
            current_commit_info = None
            current_files = []

            for line in result.stdout.split('\n'):
                if not line.strip():
                    if current_commit_info:
                        # Create commit with collected files
                        parts = current_commit_info.split('|')
                        if len(parts) == 4:
                            commit = GitCommit(
                                hash=parts[0],
                                author=parts[1],
                                date=datetime.fromisoformat(parts[2]),
                                message=parts[3],
                                files=current_files.copy()
                            )
                            commits.append(commit)
                        current_commit_info = None
                        current_files = []
                    continue

                if '|' in line:
                    # This is commit info
                    current_commit_info = line
                else:
                    # This is a file
                    current_files.append(line)

            # Handle last commit
            if current_commit_info:
                parts = current_commit_info.split('|')
                if len(parts) == 4:
                    commit = GitCommit(
                        hash=parts[0],
                        author=parts[1],
                        date=datetime.fromisoformat(parts[2]),
                        message=parts[3],
                        files=current_files
                    )
                    commits.append(commit)

            self.logger.info(f"Retrieved {len(commits)} commits")
            return commits

        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error getting commits: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return []

    def get_commit_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the repository.

        Returns:
            Dictionary with repository statistics
        """
        if not self.is_git_repo():
            return {}

        stats = {
            "total_commits": 0,
            "contributors": [],
            "first_commit_date": None,
            "last_commit_date": None,
            "branches": [],
            "tags": [],
        }

        try:
            # Count commits
            result = subprocess.run(
                ["git", "-C", str(self.repo_path), "rev-list", "--count", "HEAD"],
                capture_output=True,
                text=True,
                check=True
            )
            stats["total_commits"] = int(result.stdout.strip())

            # Get contributors
            result = subprocess.run(
                ["git", "-C", str(self.repo_path), "log", "--format=%an"],
                capture_output=True,
                text=True,
                check=True
            )
            contributors = set(line.strip() for line in result.stdout.split('\n') if line.strip())
            stats["contributors"] = sorted(list(contributors))

            # Get first commit date
            result = subprocess.run(
                ["git", "-C", str(self.repo_path), "log", "--reverse", "--format=%ai", "--max-count=1"],
                capture_output=True,
                text=True,
                check=True
            )
            if result.stdout.strip():
                stats["first_commit_date"] = result.stdout.strip()

            # Get last commit date
            result = subprocess.run(
                ["git", "-C", str(self.repo_path), "log", "--format=%ai", "--max-count=1"],
                capture_output=True,
                text=True,
                check=True
            )
            if result.stdout.strip():
                stats["last_commit_date"] = result.stdout.strip()

            # Get branches
            result = subprocess.run(
                ["git", "-C", str(self.repo_path), "branch", "-a"],
                capture_output=True,
                text=True,
                check=True
            )
            branches = [line.strip().replace('* ', '') for line in result.stdout.split('\n') if line.strip()]
            stats["branches"] = branches

            # Get tags
            result = subprocess.run(
                ["git", "-C", str(self.repo_path), "tag"],
                capture_output=True,
                text=True,
                check=True
            )
            tags = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            stats["tags"] = tags

        except Exception as e:
            self.logger.error(f"Error getting commit stats: {e}")

        return stats

    def analyze_development_phases(self, commits: List[GitCommit]) -> List[Dict[str, Any]]:
        """
        Analyze development phases based on commit messages.

        Args:
            commits: List of commits

        Returns:
            List of development phases with analysis
        """
        phases = []
        keywords = {
            "initial": ["initial", "init", "start", "setup", "first"],
            "feature": ["add", "implement", "feature", "new"],
            "fix": ["fix", "bug", "issue", "resolve"],
            "refactor": ["refactor", "refactoring", "restructure", "improve"],
            "test": ["test", "testing", "spec"],
            "docs": ["docs", "documentation", "readme"],
            "performance": ["performance", "optimize", "speed"],
        }

        phase_counts = {phase: 0 for phase in keywords.keys()}

        for commit in commits:
            message_lower = commit.message.lower()
            for phase, phase_keywords in keywords.items():
                if any(keyword in message_lower for keyword in phase_keywords):
                    phase_counts[phase] += 1
                    break

        # Create phase analysis
        for phase, count in phase_counts.items():
            if count > 0:
                phases.append({
                    "phase": phase,
                    "commits": count,
                    "percentage": (count / len(commits) * 100) if commits else 0
                })

        return sorted(phases, key=lambda x: x["commits"], reverse=True)
