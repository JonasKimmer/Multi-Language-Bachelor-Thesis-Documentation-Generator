"""Documentation chapter generator using Claude API."""

import logging
from pathlib import Path
from typing import Dict, Any, List
from .utils.claude_client import ClaudeClient

logger = logging.getLogger(__name__)


class ChapterGenerator:
    """Generates documentation chapters using Claude API."""

    def __init__(self, claude_client: ClaudeClient, config: Dict[str, Any]):
        """
        Initialize chapter generator.

        Args:
            claude_client: Claude API client
            config: Configuration dictionary
        """
        self.claude = claude_client
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Get configuration values
        self.language = config.get('output', {}).get('language', 'de')
        self.target_words = config.get('output', {}).get('chapter_length', 600)
        self.include_code_examples = config.get('documentation', {}).get('include_code_examples', True)

    def generate_executive_summary(self, context: Dict[str, Any]) -> str:
        """Generate executive summary chapter."""
        template = """Erstelle eine Executive Summary (Zusammenfassung) für dieses Projekt.

Die Summary soll enthalten:
1. **Projektziel**: Was ist der Zweck des Projekts?
2. **Technologie-Stack**: Welche Haupttechnologien werden verwendet?
3. **Hauptfunktionen**: Was sind die 3-5 wichtigsten Features?
4. **Umfang**: Größe des Projekts (LOC, Anzahl Module, etc.)
5. **Status**: Entwicklungsstand

Zielgruppe: Professor/Betreuer, der einen schnellen Überblick braucht."""

        return self.claude.generate_chapter(
            chapter_name="Executive Summary",
            context=context,
            template=template,
            language=self.language,
            target_words=self.target_words
        )

    def generate_system_architecture(self, context: Dict[str, Any]) -> str:
        """Generate system architecture chapter."""
        template = """Erstelle das Kapitel "Systemarchitektur".

Das Kapitel soll enthalten:
1. **Komponenten-Übersicht**: Welche Hauptkomponenten gibt es?
2. **Tech-Stack mit Begründung**: Welche Technologien/Frameworks werden verwendet und WARUM?
3. **Architektur-Pattern**: Welches Architekturmuster wird verwendet (MVC, Microservices, etc.)?
4. **Datenfluss**: Wie fließen Daten durch das System?
5. **Externe Abhängigkeiten**: Welche externen Services/Libraries werden genutzt?

Wichtig:
- Erkläre WARUM diese Architektur gewählt wurde
- Nenne Alternativen die NICHT gewählt wurden
- Begründe technische Entscheidungen"""

        return self.claude.generate_chapter(
            chapter_name="Systemarchitektur",
            context=context,
            template=template,
            language=self.language,
            target_words=self.target_words
        )

    def generate_code_structure(self, context: Dict[str, Any]) -> str:
        """Generate code structure & design chapter."""
        template = """Erstelle das Kapitel "Code-Struktur & Design".

Das Kapitel soll enthalten:
1. **Modul/Package-Struktur**: Wie ist der Code organisiert?
2. **Wichtigste Klassen/Komponenten**: Was sind die Kern-Klassen?
3. **Design-Patterns**: Welche Design-Patterns werden verwendet?
4. **Namenskonventionen**: Welche Konventionen werden befolgt?
5. **Code-Organisation**: Wie sind Concerns getrennt?

Wichtig:
- Zeige konkrete Beispiele aus dem Code
- Erkläre WARUM diese Struktur gewählt wurde
- Bewerte die Wartbarkeit und Erweiterbarkeit"""

        return self.claude.generate_chapter(
            chapter_name="Code-Struktur & Design",
            context=context,
            template=template,
            language=self.language,
            target_words=self.target_words
        )

    def generate_implementation_chronology(self, context: Dict[str, Any]) -> str:
        """Generate implementation chronology chapter."""
        template = """Erstelle das Kapitel "Implementierungs-Chronologie".

Das Kapitel soll enthalten:
1. **Entwicklungsphasen**: In welcher Reihenfolge wurde entwickelt?
2. **Begründung der Reihenfolge**: WARUM wurde in dieser Reihenfolge entwickelt?
   - Technische Abhängigkeiten
   - Risiko-Management
   - Prioritäten
3. **Meilensteine**: Was waren wichtige Entwicklungs-Meilensteine?
4. **Iterationen**: Wie wurde iterativ entwickelt?

Wichtig:
- Basiere die Analyse auf der Git-History
- Erkläre die LOGIK hinter der Entwicklungsreihenfolge
- NICHT nur auflisten WAS gemacht wurde, sondern WARUM in dieser Reihenfolge"""

        return self.claude.generate_chapter(
            chapter_name="Implementierungs-Chronologie",
            context=context,
            template=template,
            language=self.language,
            target_words=self.target_words
        )

    def generate_technical_decisions(self, context: Dict[str, Any]) -> str:
        """Generate technical decisions chapter."""
        template = """Erstelle das Kapitel "Technische Entscheidungen".

Das Kapitel soll enthalten:
Für jede wichtige technische Entscheidung:

1. **Datenbank-Wahl**
   - WAS wurde entschieden
   - Welche ALTERNATIVEN gab es
   - WARUM diese Wahl (Vor-/Nachteile)

2. **Framework-Wahl**
   - WAS wurde entschieden
   - Welche ALTERNATIVEN gab es
   - WARUM diese Wahl

3. **Architektur-Entscheidungen**
   - WAS wurde entschieden
   - Welche ALTERNATIVEN gab es
   - WARUM diese Wahl

4. **Andere wichtige Entscheidungen**
   - Testing-Strategie
   - Deployment-Strategie
   - etc.

Wichtig:
- Objektive Bewertung
- Konkrete Vor-/Nachteile nennen
- Bezug zu Projekt-Anforderungen"""

        return self.claude.generate_chapter(
            chapter_name="Technische Entscheidungen",
            context=context,
            template=template,
            language=self.language,
            target_words=self.target_words
        )

    def generate_feature_backlog(self, context: Dict[str, Any]) -> str:
        """Generate feature backlog & prioritization chapter."""
        template = """Erstelle das Kapitel "Feature-Backlog & Priorisierung".

Das Kapitel soll enthalten:
1. **Implementierte Features**: Was wurde implementiert?
2. **Priorisierungs-Logik**: Nach welchen Kriterien wurde priorisiert?
   - Must-Have vs. Nice-to-Have
   - Business-Value
   - Technische Abhängigkeiten
3. **Scope-Management**: Was wurde bewusst NICHT implementiert?
4. **Feature-Kategorisierung**: Wie lassen sich Features gruppieren?

Wichtig:
- Erkläre die LOGIK hinter der Priorisierung
- Zeige bewusstes Scope-Management
- Begründe was weggelassen wurde"""

        return self.claude.generate_chapter(
            chapter_name="Feature-Backlog & Priorisierung",
            context=context,
            template=template,
            language=self.language,
            target_words=self.target_words
        )

    def generate_value_analysis(self, context: Dict[str, Any]) -> str:
        """Generate value analysis chapter."""
        template = """Erstelle das Kapitel "Mehrwert-Analyse".

Das Kapitel soll enthalten:
1. **Problem-Definition**: Welches Problem wird gelöst?
   - Ausgangssituation
   - Pain-Points
   - Bedarf

2. **Lösungs-Ansatz**: Wie wird das Problem gelöst?
   - Kern-Funktionalität
   - Innovation
   - Technischer Ansatz

3. **Quantifizierbarer Nutzen**:
   - Zeit-Ersparnis
   - Kosten-Reduktion
   - Qualitäts-Verbesserung
   - Konkrete Zahlen/Metriken

4. **Innovation & Differenzierung**:
   - Was ist NEU/BESSER als existierende Lösungen?
   - Unique Selling Points
   - Technologische Innovation

Wichtig:
- Sei KONKRET und quantifizierbar
- Vergleiche mit Alternativen
- Zeige echten Mehrwert"""

        return self.claude.generate_chapter(
            chapter_name="Mehrwert-Analyse",
            context=context,
            template=template,
            language=self.language,
            target_words=self.target_words
        )

    def generate_methodology(self, context: Dict[str, Any]) -> str:
        """Generate methodology chapter."""
        template = """Erstelle das Kapitel "Methodisches Vorgehen".

Das Kapitel soll enthalten:
1. **Entwicklungsmethodik**: Welche Methodik wurde verwendet?
   - Agile/Scrum/Kanban/Waterfall?
   - Warum diese Wahl?

2. **Testing-Strategie**:
   - Welche Test-Arten werden verwendet?
   - Test-Coverage
   - Testing-Tools

3. **Tools & Workflows**:
   - Entwicklungstools
   - Version Control
   - CI/CD
   - Code Review

4. **Qualitätssicherung**:
   - Code-Qualität
   - Standards
   - Best Practices

Wichtig:
- Konkrete Tools und Prozesse nennen
- Begründe die Wahl der Methodik
- Zeige wie Qualität sichergestellt wird"""

        return self.claude.generate_chapter(
            chapter_name="Methodisches Vorgehen",
            context=context,
            template=template,
            language=self.language,
            target_words=self.target_words
        )

    def generate_all_chapters(
        self,
        context: Dict[str, Any],
        output_dir: Path,
        progress_callback=None
    ) -> Dict[str, str]:
        """
        Generate all documentation chapters.

        Args:
            context: Context data for generation
            output_dir: Directory to save chapters
            progress_callback: Optional callback for progress updates

        Returns:
            Dictionary mapping chapter names to file paths
        """
        chapters = {
            "00_executive_summary": self.generate_executive_summary,
            "01_systemarchitektur": self.generate_system_architecture,
            "02_code_struktur": self.generate_code_structure,
            "03_implementierung_chronologie": self.generate_implementation_chronology,
            "04_technische_entscheidungen": self.generate_technical_decisions,
            "05_feature_backlog": self.generate_feature_backlog,
            "06_mehrwert_analyse": self.generate_value_analysis,
            "07_methodik": self.generate_methodology,
        }

        generated_chapters = {}

        for i, (filename, generator_func) in enumerate(chapters.items(), 1):
            try:
                if progress_callback:
                    progress_callback(i, len(chapters), f"Generating {filename}")

                self.logger.info(f"Generating chapter: {filename}")
                content = generator_func(context)

                # Save chapter
                chapter_path = output_dir / f"{filename}.md"
                chapter_path.write_text(content, encoding='utf-8')

                generated_chapters[filename] = str(chapter_path)
                self.logger.info(f"Saved chapter: {chapter_path}")

            except Exception as e:
                self.logger.error(f"Error generating {filename}: {e}")

        return generated_chapters

    def combine_chapters(self, chapter_files: Dict[str, str], output_path: Path) -> None:
        """
        Combine all chapters into a single document.

        Args:
            chapter_files: Dictionary mapping chapter names to file paths
            output_path: Path for combined document
        """
        combined_content = []

        # Add title
        project_name = self.config.get('project', {}).get('name', 'Project')
        combined_content.append(f"# Technische Dokumentation: {project_name}\n\n")

        # Add metadata
        author = self.config.get('project', {}).get('author', '')
        university = self.config.get('project', {}).get('university', '')
        year = self.config.get('project', {}).get('year', '')

        if author or university or year:
            combined_content.append("## Metadata\n\n")
            if author:
                combined_content.append(f"**Autor:** {author}\n\n")
            if university:
                combined_content.append(f"**Hochschule:** {university}\n\n")
            if year:
                combined_content.append(f"**Jahr:** {year}\n\n")
            combined_content.append("---\n\n")

        # Add each chapter
        for chapter_name in sorted(chapter_files.keys()):
            chapter_path = Path(chapter_files[chapter_name])
            if chapter_path.exists():
                content = chapter_path.read_text(encoding='utf-8')
                combined_content.append(content)
                combined_content.append("\n\n---\n\n")

        # Write combined document
        output_path.write_text(''.join(combined_content), encoding='utf-8')
        self.logger.info(f"Combined document saved to: {output_path}")
