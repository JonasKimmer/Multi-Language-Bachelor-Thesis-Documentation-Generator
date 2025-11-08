#!/usr/bin/env python3
"""
Multi-Language Bachelor Thesis Documentation Generator

Automatically generates scientific technical documentation for bachelor theses
from code repositories.
"""

import argparse
import logging
import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional
import yaml

from thesis_doc_gen.analyzers.factory import AnalyzerFactory
from thesis_doc_gen.utils.git_parser import GitParser
from thesis_doc_gen.utils.file_scanner import FileScanner
from thesis_doc_gen.utils.claude_client import ClaudeClient
from thesis_doc_gen.utils.diagram_generator import DiagramGenerator
from thesis_doc_gen.chapter_generator import ChapterGenerator


# Configure logging
def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('thesis_doc_gen.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def load_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    if not config_path.exists():
        print(f"Config file not found: {config_path}")
        print("Using default configuration...")
        return get_default_config()

    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    return config


def get_default_config() -> Dict[str, Any]:
    """Get default configuration."""
    return {
        'project': {
            'name': 'Project',
            'author': 'Author',
            'supervisor': 'Supervisor',
            'university': 'University',
            'year': 2025
        },
        'analysis': {
            'languages': 'auto',
            'focus_areas': ['architecture', 'design_decisions', 'methodology'],
            'exclude_paths': FileScanner.DEFAULT_EXCLUDE,
            'max_file_size_kb': 500
        },
        'output': {
            'format': ['markdown'],
            'language': 'de',
            'chapter_length': 600
        },
        'documentation': {
            'style': 'academic',
            'include_code_examples': True,
            'max_code_lines_per_example': 30
        }
    }


def print_progress(step: int, total: int, message: str):
    """Print progress message."""
    print(f"[{step}/{total}] {message}...")


def analyze_repository(repo_path: Path, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze the repository.

    Args:
        repo_path: Path to repository
        config: Configuration dictionary

    Returns:
        Dictionary with analysis results
    """
    logger = logging.getLogger(__name__)
    context = {
        'project': config.get('project', {}),
        'repository': {},
        'git_history': {},
        'analysis': {},
        'statistics': {}
    }

    # Step 1: Scan file structure
    print_progress(1, 7, "Analyzing repository structure")
    scanner = FileScanner(
        repo_path,
        exclude_paths=config.get('analysis', {}).get('exclude_paths', []),
        max_file_size_kb=config.get('analysis', {}).get('max_file_size_kb', 500)
    )

    scan_result = scanner.scan()
    context['repository'] = {
        'total_files': scan_result['total_files'],
        'total_directories': scan_result['total_directories'],
        'project_types': scanner.get_project_type(),
        'size_category': scanner.estimate_project_size(),
        'config_files': scanner.find_config_files()
    }

    logger.info(f"Found {scan_result['total_files']} files in {scan_result['total_directories']} directories")

    # Step 2: Extract Git history
    print_progress(2, 7, "Extracting Git history")
    git_parser = GitParser(repo_path)

    if git_parser.is_git_repo():
        commits = git_parser.get_commits(limit=150)
        stats = git_parser.get_commit_stats()
        phases = git_parser.analyze_development_phases(commits)

        context['git_history'] = {
            'total_commits': len(commits),
            'contributors': stats.get('contributors', []),
            'first_commit_date': stats.get('first_commit_date'),
            'last_commit_date': stats.get('last_commit_date'),
            'development_phases': phases,
            'recent_commits': [c.to_dict() for c in commits[:10]]
        }

        logger.info(f"Extracted {len(commits)} commits")
    else:
        logger.warning("No Git repository found - skipping Git analysis")
        context['git_history'] = {'note': 'No Git repository found'}

    # Step 3: Analyze code by language
    languages = config.get('analysis', {}).get('languages', 'auto')
    if isinstance(languages, str):
        languages = [languages]

    print_progress(3, 7, f"Analyzing code ({', '.join(languages)})")

    analysis_results = AnalyzerFactory.analyze_repository(
        repo_path,
        languages=languages,
        exclude_paths=config.get('analysis', {}).get('exclude_paths', [])
    )

    # Convert analysis results to dictionary format
    context['analysis'] = {}
    all_dependencies = []

    for language, result in analysis_results.items():
        result_dict = result.to_dict()
        context['analysis'][language] = {
            'files_analyzed': len(result.files_analyzed),
            'total_lines': result.total_lines,
            'classes_count': len(result.classes),
            'functions_count': len(result.functions),
            'dependencies': result.dependencies[:20],  # Limit to top 20
        }
        all_dependencies.extend(result.dependencies)

        logger.info(f"Analyzed {len(result.files_analyzed)} {language} files ({result.total_lines} lines)")

    # Step 4: Calculate statistics
    print_progress(4, 7, "Calculating code statistics")

    total_lines = sum(r.total_lines for r in analysis_results.values())
    language_distribution = {
        lang: {
            'lines': result.total_lines,
            'percentage': (result.total_lines / total_lines * 100) if total_lines > 0 else 0
        }
        for lang, result in analysis_results.items()
    }

    context['statistics'] = {
        'total_lines': total_lines,
        'language_distribution': language_distribution,
        'unique_dependencies': len(set(all_dependencies)),
        'files_by_extension': scan_result.get('files_by_extension', {})
    }

    return context, analysis_results


def generate_documentation(
    context: Dict[str, Any],
    analysis_results: Dict[str, Any],
    config: Dict[str, Any],
    output_dir: Path,
    dry_run: bool = False
) -> None:
    """
    Generate documentation.

    Args:
        context: Analysis context
        analysis_results: Code analysis results
        config: Configuration
        output_dir: Output directory
        dry_run: If True, don't actually generate (just show what would be done)
    """
    if dry_run:
        print("\n=== DRY RUN MODE ===")
        print("Would generate the following:")
        print(f"  - Output directory: {output_dir}")
        print(f"  - 8 documentation chapters")
        print(f"  - Up to 5 diagrams")
        print(f"  - Combined documentation file")
        print(f"  - Code statistics JSON files")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 5: Generate diagrams
    print_progress(5, 7, "Generating diagrams")
    diagram_gen = DiagramGenerator()
    diagrams = diagram_gen.generate_all_diagrams(
        analysis_results,
        context,
        output_dir
    )

    # Step 6: Generate documentation chapters
    print_progress(6, 7, "Generating documentation chapters (this may take a few minutes)")

    try:
        claude_client = ClaudeClient()
        chapter_gen = ChapterGenerator(claude_client, config)

        def chapter_progress(current, total, message):
            print(f"  [{current}/{total}] {message}...")

        chapters = chapter_gen.generate_all_chapters(
            context,
            output_dir,
            progress_callback=chapter_progress
        )

        # Combine chapters
        combined_path = output_dir / "vollstaendige_dokumentation.md"
        chapter_gen.combine_chapters(chapters, combined_path)

    except ValueError as e:
        print(f"\nError: {e}")
        print("Please set ANTHROPIC_API_KEY environment variable")
        sys.exit(1)
    except Exception as e:
        print(f"\nError generating documentation: {e}")
        logging.exception("Documentation generation failed")
        sys.exit(1)

    # Step 7: Export statistics
    print_progress(7, 7, "Exporting statistics")
    stats_dir = output_dir / "code_stats"
    stats_dir.mkdir(exist_ok=True)

    # Language distribution
    with open(stats_dir / "language_distribution.json", 'w') as f:
        json.dump(context['statistics'].get('language_distribution', {}), f, indent=2)

    # Repository info
    with open(stats_dir / "repository_info.json", 'w') as f:
        json.dump(context['repository'], f, indent=2)

    print("\n✓ Documentation successfully generated!")
    print(f"\nOutput directory: {output_dir.absolute()}")
    print(f"  - {len(chapters)} chapters")
    print(f"  - {len(diagrams)} diagrams")
    print(f"  - Combined document: {combined_path.name}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Multi-Language Bachelor Thesis Documentation Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --repo-path ./my-project --output ./docs
  %(prog)s --repo-path ~/projects/app --config config.yaml --verbose
  %(prog)s --repo-path . --output ./thesis-docs --dry-run
        """
    )

    parser.add_argument(
        '--repo-path',
        type=Path,
        required=True,
        help='Path to the code repository'
    )

    parser.add_argument(
        '--output',
        type=Path,
        default=Path('./docs'),
        help='Output directory for documentation (default: ./docs)'
    )

    parser.add_argument(
        '--config',
        type=Path,
        default=Path('config.yaml'),
        help='Path to configuration file (default: config.yaml)'
    )

    parser.add_argument(
        '--languages',
        type=str,
        help='Comma-separated list of languages to analyze (default: auto-detect)'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without actually generating'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    # Validate repository path
    if not args.repo_path.exists():
        print(f"Error: Repository path does not exist: {args.repo_path}")
        sys.exit(1)

    if not args.repo_path.is_dir():
        print(f"Error: Repository path is not a directory: {args.repo_path}")
        sys.exit(1)

    # Load configuration
    config = load_config(args.config)

    # Override languages if specified
    if args.languages:
        config['analysis']['languages'] = args.languages.split(',')

    # Print header
    print("=" * 60)
    print("Multi-Language Bachelor Thesis Documentation Generator")
    print("=" * 60)
    print(f"Repository: {args.repo_path.absolute()}")
    print(f"Output: {args.output.absolute()}")
    print(f"Config: {args.config}")
    print("=" * 60)
    print()

    # Analyze repository
    try:
        context, analysis_results = analyze_repository(args.repo_path, config)

        # Generate documentation
        generate_documentation(
            context,
            analysis_results,
            config,
            args.output,
            dry_run=args.dry_run
        )

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.exception("Fatal error")
        print(f"\nFatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
