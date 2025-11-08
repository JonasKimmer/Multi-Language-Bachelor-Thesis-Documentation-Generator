"""Claude API client for generating documentation content."""

import os
import time
import logging
from typing import Optional, Dict, Any
import anthropic

logger = logging.getLogger(__name__)


class ClaudeClient:
    """Client for interacting with Claude API."""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize the Claude API client.

        Args:
            api_key: Anthropic API key (defaults to environment variable)
            model: Claude model to use
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment or provided")

        self.model = model
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.logger = logging.getLogger(__name__)

        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Minimum seconds between requests

    def generate_content(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 8000,
        temperature: float = 0.7,
        retry_count: int = 3
    ) -> str:
        """
        Generate content using Claude API.

        Args:
            prompt: The prompt to send to Claude
            system_prompt: System prompt for context
            max_tokens: Maximum tokens to generate
            temperature: Temperature for generation (0.0 to 1.0)
            retry_count: Number of retries on failure

        Returns:
            Generated text content
        """
        # Rate limiting
        time_since_last = time.time() - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)

        for attempt in range(retry_count):
            try:
                self.logger.info(f"Generating content (attempt {attempt + 1}/{retry_count})")

                # Build messages
                messages = [{"role": "user", "content": prompt}]

                # Make API call
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=system_prompt if system_prompt else "You are a technical documentation expert for scientific bachelor theses.",
                    messages=messages
                )

                self.last_request_time = time.time()

                # Extract text from response
                if response.content and len(response.content) > 0:
                    return response.content[0].text

                self.logger.warning("Empty response from Claude API")
                return ""

            except anthropic.RateLimitError as e:
                self.logger.warning(f"Rate limit hit: {e}")
                if attempt < retry_count - 1:
                    wait_time = (attempt + 1) * 5  # Exponential backoff
                    self.logger.info(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    raise

            except anthropic.APIError as e:
                self.logger.error(f"API error: {e}")
                if attempt < retry_count - 1:
                    time.sleep(2)
                else:
                    raise

            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                if attempt < retry_count - 1:
                    time.sleep(2)
                else:
                    raise

        return ""

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
        system_prompt = f"""Du bist ein Experte für technische Dokumentation wissenschaftlicher Bachelorarbeiten.

Anforderungen:
- Schreibe auf Bachelor-Niveau (wissenschaftlich präzise, aber verständlich)
- Verwende korrekte Fachbegriffe
- Begründe Aussagen objektiv
- Zielsprache: {language.upper()}
- Zielumfang: ca. {target_words} Wörter
- Format: Markdown

Stil:
- Sachlich und objektiv
- Präzise und konkret
- Mit Begründungen (nicht nur Behauptungen)
- Zeige technische Tiefe"""

        prompt = f"""Erstelle das Kapitel: {chapter_name}

{template}

Verfügbare Kontextdaten:
{self._format_context(context)}

Anforderungen:
- Schreibe wissenschaftlich fundiert auf Bachelor-Niveau
- Erkläre nicht nur WAS gemacht wurde, sondern auch WARUM
- Bei Entscheidungen: Nenne Alternativen und Begründung
- Füge konkrete Code-Beispiele ein wo sinnvoll
- Verwende Markdown-Formatierung
- Zielumfang: {target_words} Wörter

Generiere jetzt das vollständige Kapitel:"""

        return self.generate_content(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=16000,
            temperature=0.7
        )

    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context data for the prompt."""
        lines = []

        for key, value in context.items():
            if isinstance(value, dict):
                lines.append(f"\n## {key}:")
                for sub_key, sub_value in value.items():
                    lines.append(f"  - {sub_key}: {sub_value}")
            elif isinstance(value, list):
                lines.append(f"\n## {key}:")
                for item in value[:10]:  # Limit to first 10 items
                    lines.append(f"  - {item}")
                if len(value) > 10:
                    lines.append(f"  ... and {len(value) - 10} more")
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

        # Common patterns for sensitive data
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

    def estimate_tokens(self, text: str) -> int:
        """
        Estimate the number of tokens in text.

        Args:
            text: Text to estimate

        Returns:
            Estimated token count
        """
        # Rough estimation: ~4 characters per token
        return len(text) // 4

    def chunk_content(self, content: str, max_chunk_size: int = 100000) -> list[str]:
        """
        Split content into chunks for API calls.

        Args:
            content: Content to chunk
            max_chunk_size: Maximum characters per chunk

        Returns:
            List of content chunks
        """
        if len(content) <= max_chunk_size:
            return [content]

        chunks = []
        lines = content.split('\n')
        current_chunk = []
        current_size = 0

        for line in lines:
            line_size = len(line) + 1  # +1 for newline
            if current_size + line_size > max_chunk_size and current_chunk:
                chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
                current_size = line_size
            else:
                current_chunk.append(line)
                current_size += line_size

        if current_chunk:
            chunks.append('\n'.join(current_chunk))

        return chunks
