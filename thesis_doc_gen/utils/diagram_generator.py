"""Mermaid diagram generator for documentation."""

import logging
from typing import Dict, List, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class DiagramGenerator:
    """Generates Mermaid diagrams from code analysis."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def generate_class_diagram(self, analysis_results: Dict[str, Any]) -> str:
        """
        Generate a class diagram from analysis results.

        Args:
            analysis_results: Analysis results from language analyzers

        Returns:
            Mermaid diagram syntax
        """
        lines = ["```mermaid", "classDiagram"]

        # Process each language's classes
        for language, result in analysis_results.items():
            if hasattr(result, 'classes'):
                classes = result.classes
            elif isinstance(result, dict) and 'classes' in result:
                classes = result['classes']
            else:
                continue

            for class_info in classes[:20]:  # Limit to 20 classes for readability
                class_name = class_info.get('name', 'Unknown')

                # Add class
                lines.append(f"    class {class_name} {{")

                # Add methods
                methods = class_info.get('methods', [])
                for method in methods[:10]:  # Limit methods
                    method_name = method.get('name', '')
                    if method_name and not method_name.startswith('__'):
                        visibility = '-' if method.get('is_private') else '+'
                        lines.append(f"        {visibility}{method_name}()")

                lines.append("    }")

                # Add inheritance
                if 'extends' in class_info and class_info['extends']:
                    parent = class_info['extends']
                    lines.append(f"    {parent} <|-- {class_name}")

                # Add implementations
                if 'implements' in class_info:
                    for interface in class_info.get('implements', []):
                        if interface:
                            lines.append(f"    {interface} <|.. {class_name}")

        lines.append("```")
        return "\n".join(lines)

    def generate_architecture_diagram(self, project_info: Dict[str, Any]) -> str:
        """
        Generate an architecture diagram.

        Args:
            project_info: Project information including components

        Returns:
            Mermaid diagram syntax
        """
        lines = ["```mermaid", "graph TB"]

        # Detect components based on project structure
        components = self._detect_components(project_info)

        # Add components
        for i, component in enumerate(components):
            comp_id = f"COMP{i}"
            comp_name = component['name']
            comp_type = component.get('type', 'component')

            if comp_type == 'frontend':
                lines.append(f"    {comp_id}[{comp_name}]:::frontend")
            elif comp_type == 'backend':
                lines.append(f"    {comp_id}[{comp_name}]:::backend")
            elif comp_type == 'database':
                lines.append(f"    {comp_id}[({comp_name})]:::database")
            else:
                lines.append(f"    {comp_id}[{comp_name}]")

        # Add relationships
        if len(components) >= 2:
            for i in range(len(components) - 1):
                lines.append(f"    COMP{i} --> COMP{i+1}")

        # Add styles
        lines.append("    classDef frontend fill:#e1f5ff,stroke:#01579b")
        lines.append("    classDef backend fill:#f3e5f5,stroke:#4a148c")
        lines.append("    classDef database fill:#fff3e0,stroke:#e65100")

        lines.append("```")
        return "\n".join(lines)

    def generate_sequence_diagram(self, main_flow: List[str]) -> str:
        """
        Generate a sequence diagram for main use case.

        Args:
            main_flow: List of steps in the main flow

        Returns:
            Mermaid diagram syntax
        """
        lines = ["```mermaid", "sequenceDiagram"]
        lines.append("    participant User")
        lines.append("    participant Frontend")
        lines.append("    participant Backend")
        lines.append("    participant Database")

        # Add generic flow
        lines.append("    User->>Frontend: Request")
        lines.append("    Frontend->>Backend: API Call")
        lines.append("    Backend->>Database: Query")
        lines.append("    Database-->>Backend: Data")
        lines.append("    Backend-->>Frontend: Response")
        lines.append("    Frontend-->>User: Display")

        lines.append("```")
        return "\n".join(lines)

    def generate_er_diagram(self, sql_analysis: Dict[str, Any]) -> str:
        """
        Generate an ER diagram from SQL analysis.

        Args:
            sql_analysis: SQL analysis results

        Returns:
            Mermaid diagram syntax
        """
        lines = ["```mermaid", "erDiagram"]

        # Extract tables
        tables = []
        if isinstance(sql_analysis, dict) and 'tables' in sql_analysis:
            tables = sql_analysis['tables']
        elif hasattr(sql_analysis, 'tables'):
            tables = sql_analysis.tables

        # Add tables (simplified - real implementation would need schema info)
        for table in tables[:15]:  # Limit to 15 tables
            lines.append(f"    {table} {{")
            lines.append(f"        int id PK")
            lines.append(f"        string name")
            lines.append("    }")

        # Add some example relationships if multiple tables exist
        if len(tables) >= 2:
            lines.append(f"    {tables[0]} ||--o{{ {tables[1]} : has")

        lines.append("```")
        return "\n".join(lines)

    def generate_dependency_graph(self, dependencies: List[str]) -> str:
        """
        Generate a dependency graph.

        Args:
            dependencies: List of dependencies

        Returns:
            Mermaid diagram syntax
        """
        lines = ["```mermaid", "graph LR"]
        lines.append("    PROJECT[Project]")

        # Add dependencies (limit to top 15)
        for i, dep in enumerate(dependencies[:15]):
            dep_id = f"DEP{i}"
            # Clean up dependency name
            dep_name = dep.split('.')[0] if '.' in dep else dep
            lines.append(f"    {dep_id}[{dep_name}]")
            lines.append(f"    PROJECT --> {dep_id}")

        lines.append("```")
        return "\n".join(lines)

    def _detect_components(self, project_info: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Detect architectural components from project info.

        Args:
            project_info: Project information

        Returns:
            List of detected components
        """
        components = []

        # Detect frontend
        if self._has_frontend(project_info):
            components.append({
                'name': 'Frontend',
                'type': 'frontend'
            })

        # Detect backend
        if self._has_backend(project_info):
            components.append({
                'name': 'Backend API',
                'type': 'backend'
            })

        # Detect database
        if self._has_database(project_info):
            components.append({
                'name': 'Database',
                'type': 'database'
            })

        # If no specific components detected, add generic ones
        if not components:
            components = [
                {'name': 'Application', 'type': 'component'},
                {'name': 'Core Logic', 'type': 'component'},
            ]

        return components

    def _has_frontend(self, project_info: Dict[str, Any]) -> bool:
        """Check if project has frontend components."""
        frontend_indicators = [
            'javascript', 'typescript', 'react', 'vue', 'angular',
            'html', 'css', 'index.html', 'package.json'
        ]
        return any(indicator in str(project_info).lower() for indicator in frontend_indicators)

    def _has_backend(self, project_info: Dict[str, Any]) -> bool:
        """Check if project has backend components."""
        backend_indicators = [
            'python', 'java', 'node', 'express', 'django', 'flask',
            'spring', 'api', 'server'
        ]
        return any(indicator in str(project_info).lower() for indicator in backend_indicators)

    def _has_database(self, project_info: Dict[str, Any]) -> bool:
        """Check if project has database components."""
        database_indicators = [
            'sql', 'database', 'mysql', 'postgresql', 'mongodb',
            'sqlite', 'redis', 'db'
        ]
        return any(indicator in str(project_info).lower() for indicator in database_indicators)

    def generate_all_diagrams(
        self,
        analysis_results: Dict[str, Any],
        project_info: Dict[str, Any],
        output_dir: Path
    ) -> Dict[str, str]:
        """
        Generate all diagrams and save to files.

        Args:
            analysis_results: Analysis results from all languages
            project_info: Overall project information
            output_dir: Directory to save diagrams

        Returns:
            Dictionary mapping diagram names to file paths
        """
        diagrams_dir = output_dir / "diagrams"
        diagrams_dir.mkdir(parents=True, exist_ok=True)

        diagrams = {}

        # Class diagram
        try:
            class_diagram = self.generate_class_diagram(analysis_results)
            class_path = diagrams_dir / "class_diagram.mmd"
            class_path.write_text(class_diagram)
            diagrams["class_diagram"] = str(class_path)
            self.logger.info("Generated class diagram")
        except Exception as e:
            self.logger.error(f"Error generating class diagram: {e}")

        # Architecture diagram
        try:
            arch_diagram = self.generate_architecture_diagram(project_info)
            arch_path = diagrams_dir / "architecture.mmd"
            arch_path.write_text(arch_diagram)
            diagrams["architecture"] = str(arch_path)
            self.logger.info("Generated architecture diagram")
        except Exception as e:
            self.logger.error(f"Error generating architecture diagram: {e}")

        # Sequence diagram
        try:
            seq_diagram = self.generate_sequence_diagram([])
            seq_path = diagrams_dir / "sequence_main_flow.mmd"
            seq_path.write_text(seq_diagram)
            diagrams["sequence"] = str(seq_path)
            self.logger.info("Generated sequence diagram")
        except Exception as e:
            self.logger.error(f"Error generating sequence diagram: {e}")

        # ER diagram (if SQL detected)
        if 'SQL' in analysis_results or 'sql' in str(project_info).lower():
            try:
                sql_data = analysis_results.get('SQL', {})
                er_diagram = self.generate_er_diagram(sql_data)
                er_path = diagrams_dir / "er_diagram.mmd"
                er_path.write_text(er_diagram)
                diagrams["er_diagram"] = str(er_path)
                self.logger.info("Generated ER diagram")
            except Exception as e:
                self.logger.error(f"Error generating ER diagram: {e}")

        # Dependency graph
        try:
            all_deps = []
            for lang_result in analysis_results.values():
                if hasattr(lang_result, 'dependencies'):
                    all_deps.extend(lang_result.dependencies)
                elif isinstance(lang_result, dict) and 'dependencies' in lang_result:
                    all_deps.extend(lang_result['dependencies'])

            if all_deps:
                dep_diagram = self.generate_dependency_graph(list(set(all_deps)))
                dep_path = diagrams_dir / "dependency_graph.mmd"
                dep_path.write_text(dep_diagram)
                diagrams["dependency_graph"] = str(dep_path)
                self.logger.info("Generated dependency graph")
        except Exception as e:
            self.logger.error(f"Error generating dependency graph: {e}")

        return diagrams
