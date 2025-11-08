"""Claude API client for generating documentation content."""

import os
import time
import logging
from typing import Optional, Dict, Any
import anthropic

from .base_llm_client import BaseLLMClient

logger = logging.getLogger(__name__)


class ClaudeClient(BaseLLMClient):
    """Client for interacting with Claude API."""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize the Claude API client.

        Args:
            api_key: Anthropic API key (defaults to environment variable)
            model: Claude model to use
        """
        super().__init__(model)

        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment or provided")

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
