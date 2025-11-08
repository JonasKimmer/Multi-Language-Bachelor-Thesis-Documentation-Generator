"""Base class for LLM clients."""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients."""

    def __init__(self, model: str):
        """
        Initialize the LLM client.

        Args:
            model: Model identifier
        """
        self.model = model

    @abstractmethod
    def generate_content(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 8000,
        temperature: float = 0.7,
        retry_count: int = 3
    ) -> str:
        """
        Generate content using the LLM.

        Args:
            prompt: The prompt to send
            system_prompt: System prompt for context
            max_tokens: Maximum tokens to generate
            temperature: Temperature for generation (0.0 to 1.0)
            retry_count: Number of retries on failure

        Returns:
            Generated text content
        """
        pass

    @abstractmethod
    def estimate_tokens(self, text: str) -> int:
        """
        Estimate the number of tokens in text.

        Args:
            text: Text to estimate

        Returns:
            Estimated token count
        """
        pass

    def generate_chapter(
        self,
        chapter_name: str,
        context: Dict[str, Any],
        template: str,
        language: str = "de",
        target_words: int = 600
    ) -> str:
        """
        Generate a documentation chapter.

        Args:
            chapter_name: Name of the chapter
            context: Context data for generation
            template: Template with instructions
            language: Language for documentation (de or en)
            target_words: Target word count

        Returns:
            Generated chapter content in Markdown
        """
        system_prompt = self._create_system_prompt(language, target_words)
        prompt = self._create_chapter_prompt(chapter_name, template, context, target_words)

        return self.generate_content(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=16000,
            temperature=0.7
        )

    def _create_system_prompt(self, language: str, target_words: int) -> str:
        """Create system prompt for documentation generation."""
        if language.lower() == "de":
            return f"""Du bist ein technischer Dokumentations-Autor für Bachelorarbeiten.

🚨 KRITISCH - EXAKTE DATEN VERWENDEN:
- ERFINDE KEINE Klassennamen, Methodennamen oder Zahlen
- Nutze AUSSCHLIESSLICH die bereitgestellten Kontextdaten
- Wenn Klassen erwähnt werden: Kopiere die EXAKTEN Namen aus dem Context
- Wenn Frameworks genannt werden: Nutze NUR die erkannten Frameworks
- Bei Zahlen (Zeilen, Dateien, etc.): Nutze NUR die analysierten Werte
- KEINE generischen Beispiele - nur echte Daten aus dem Projekt

Anforderungen:
- Schreibe auf Bachelor-Niveau (wissenschaftlich präzise, aber verständlich)
- Verwende korrekte Fachbegriffe
- Begründe Aussagen objektiv basierend auf den ECHTEN Daten
- Zielsprache: DEUTSCH
- Zielumfang: ca. {target_words} Wörter
- Format: Markdown

Stil:
- Sachlich und objektiv
- Präzise und konkret (mit ECHTEN Namen/Zahlen)
- Mit Begründungen basierend auf analysierten Daten
- Zeige technische Tiefe anhand REALER Code-Strukturen"""
        else:
            return f"""You are an expert in technical documentation for bachelor theses.

Requirements:
- Write at bachelor level (scientifically precise but understandable)
- Use correct technical terms
- Justify statements objectively
- Target language: ENGLISH
- Target length: approx. {target_words} words
- Format: Markdown

Style:
- Factual and objective
- Precise and concrete
- With justifications (not just claims)
- Show technical depth"""

    def _create_chapter_prompt(
        self,
        chapter_name: str,
        template: str,
        context: Dict[str, Any],
        target_words: int
    ) -> str:
        """Create prompt for chapter generation."""
        context_str = self._format_context(context)

        return f"""Erstelle das Kapitel: {chapter_name}

{template}

📊 VERFÜGBARE KONTEXTDATEN (NUTZE NUR DIESE!):
{context_str}

🚨 KRITISCHE REGELN:
1. Nutze AUSSCHLIESSLICH die oben bereitgestellten Kontextdaten
2. Wenn du Klassen erwähnst: Kopiere die EXAKTEN Namen aus "classes:" (z.B. "ChatSession", "OllamaService")
3. Wenn du Frameworks nennst: Nutze NUR "frameworks:" Liste (z.B. FastAPI, SQLAlchemy)
4. Bei Zahlen: Nutze NUR "total_lines", "files_analyzed", etc. aus dem Context
5. ERFINDE KEINE Beispiel-Klassen wie "User", "Product", etc. - nur ECHTE aus dem Context!
6. Wenn Informationen fehlen: Schreibe "Im analysierten Code nicht gefunden" statt zu erfinden

Anforderungen:
- Schreibe wissenschaftlich fundiert auf Bachelor-Niveau
- Erkläre nicht nur WAS gemacht wurde, sondern auch WARUM
- Bei Entscheidungen: Nenne Alternativen und Begründung (basierend auf echten Daten)
- Nutze ECHTE Klassennamen und Methodennamen aus dem Context für Beispiele
- Verwende Markdown-Formatierung
- Zielumfang: {target_words} Wörter

Generiere jetzt das vollständige Kapitel MIT ECHTEN DATEN AUS DEM CONTEXT:"""

    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context data for the prompt."""
        lines = []

        for key, value in context.items():
            if isinstance(value, dict):
                lines.append(f"\n## {key}:")
                for sub_key, sub_value in value.items():
                    # Special formatting for classes and functions lists
                    if sub_key == 'classes' and isinstance(sub_value, list):
                        lines.append(f"  {sub_key}: ({len(sub_value)} Klassen gefunden)")
                        for cls in sub_value[:15]:  # Show first 15 classes
                            methods_str = ', '.join(cls.get('methods', [])[:5])
                            bases_str = ', '.join(cls.get('bases', []))
                            lines.append(f"    - {cls.get('name')}: Methoden=[{methods_str}], Erbt von=[{bases_str}]")
                        if len(sub_value) > 15:
                            lines.append(f"    ... und {len(sub_value) - 15} weitere Klassen")
                    elif sub_key == 'functions' and isinstance(sub_value, list):
                        lines.append(f"  {sub_key}: ({len(sub_value)} Funktionen gefunden)")
                        for func in sub_value[:10]:  # Show first 10 functions
                            args_str = ', '.join(func.get('args', [])[:5])
                            lines.append(f"    - {func.get('name')}({args_str})")
                        if len(sub_value) > 10:
                            lines.append(f"    ... und {len(sub_value) - 10} weitere Funktionen")
                    else:
                        lines.append(f"  - {sub_key}: {sub_value}")
            elif isinstance(value, list):
                lines.append(f"\n## {key}:")
                for item in value[:10]:  # Limit to first 10 items
                    lines.append(f"  - {item}")
                if len(value) > 10:
                    lines.append(f"  ... und {len(value) - 10} weitere")
            else:
                lines.append(f"- {key}: {value}")

        return "\n".join(lines)

    def filter_sensitive_data(self, content: str) -> str:
        """
        Filter sensitive data from content.

        Args:
            content: Content to filter

        Returns:
            Filtered content with sensitive data replaced
        """
        import re

        patterns = {
            "api_key": r'(?i)(api[_-]?key|apikey)[\s:=]+["\']?([a-zA-Z0-9_\-]+)["\']?',
            "password": r'(?i)(password|passwd|pwd)[\s:=]+["\']?([^\s"\']+)["\']?',
            "token": r'(?i)(token|auth)[\s:=]+["\']?([a-zA-Z0-9_\-\.]+)["\']?',
            "secret": r'(?i)(secret)[\s:=]+["\']?([a-zA-Z0-9_\-]+)["\']?',
        }

        filtered = content
        for pattern_name, pattern in patterns.items():
            filtered = re.sub(pattern, r'\1: ***filtered***', filtered)

        return filtered
