"""Llama 3.1 8B client using Ollama or HuggingFace."""

import os
import time
import logging
from typing import Optional
import requests
import json

from .base_llm_client import BaseLLMClient

logger = logging.getLogger(__name__)


class LlamaClient(BaseLLMClient):
    """Client for Llama 3.1 8B using Ollama (local) or HuggingFace API."""

    def __init__(
        self,
        model: str = "llama3.1:8b",
        backend: str = "ollama",
        api_key: Optional[str] = None
    ):
        """
        Initialize Llama client.

        Args:
            model: Model identifier (default: llama3.1:8b for Ollama)
            backend: Backend to use ('ollama' or 'huggingface')
            api_key: HuggingFace API key (only needed for huggingface backend)
        """
        super().__init__(model)
        self.backend = backend.lower()
        self.logger = logging.getLogger(__name__)

        if self.backend == "ollama":
            self.base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
            self._check_ollama_connection()
        elif self.backend == "huggingface":
            self.api_key = api_key or os.environ.get("HUGGINGFACE_API_KEY")
            if not self.api_key:
                raise ValueError("HUGGINGFACE_API_KEY required for HuggingFace backend")
            self.base_url = "https://api-inference.huggingface.co/models"
            self.model_name = model or "meta-llama/Meta-Llama-3.1-8B-Instruct"
        else:
            raise ValueError(f"Unknown backend: {backend}. Use 'ollama' or 'huggingface'")

        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0

    def _check_ollama_connection(self):
        """Check if Ollama is running."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                self.logger.info("Ollama connection successful")
                # Check if model is available
                models = response.json().get("models", [])
                model_names = [m.get("name") for m in models]
                if self.model not in model_names:
                    self.logger.warning(
                        f"Model {self.model} not found. Available models: {model_names}\n"
                        f"Install with: ollama pull {self.model}"
                    )
            else:
                self.logger.warning("Ollama might not be running properly")
        except Exception as e:
            self.logger.error(
                f"Cannot connect to Ollama at {self.base_url}\n"
                f"Error: {e}\n"
                f"Make sure Ollama is running: 'ollama serve'"
            )

    def generate_content(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 8000,
        temperature: float = 0.7,
        retry_count: int = 3
    ) -> str:
        """Generate content using Llama."""
        # Rate limiting
        time_since_last = time.time() - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)

        for attempt in range(retry_count):
            try:
                self.logger.info(f"Generating content (attempt {attempt + 1}/{retry_count})")

                if self.backend == "ollama":
                    response = self._generate_ollama(prompt, system_prompt, max_tokens, temperature)
                else:  # huggingface
                    response = self._generate_huggingface(prompt, system_prompt, max_tokens, temperature)

                self.last_request_time = time.time()
                return response

            except Exception as e:
                self.logger.error(f"Generation error: {e}")
                if attempt < retry_count - 1:
                    wait_time = (attempt + 1) * 2
                    self.logger.info(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    raise

        return ""

    def _generate_ollama(
        self,
        prompt: str,
        system_prompt: Optional[str],
        max_tokens: int,
        temperature: float
    ) -> str:
        """Generate using Ollama."""
        # Combine system and user prompt
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
            }
        }

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=300  # 5 minutes timeout
        )

        if response.status_code != 200:
            raise Exception(f"Ollama API error: {response.status_code} - {response.text}")

        result = response.json()
        return result.get("response", "")

    def _generate_huggingface(
        self,
        prompt: str,
        system_prompt: Optional[str],
        max_tokens: int,
        temperature: float
    ) -> str:
        """Generate using HuggingFace Inference API."""
        # Format as chat messages for Llama 3.1
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        # Convert to Llama 3.1 chat format
        formatted_prompt = self._format_llama_chat(messages)

        payload = {
            "inputs": formatted_prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "return_full_text": False,
            }
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            f"{self.base_url}/{self.model_name}",
            headers=headers,
            json=payload,
            timeout=300
        )

        if response.status_code != 200:
            raise Exception(f"HuggingFace API error: {response.status_code} - {response.text}")

        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "")
        return ""

    def _format_llama_chat(self, messages: list) -> str:
        """Format messages in Llama 3.1 chat format."""
        formatted = "<|begin_of_text|>"
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            formatted += f"<|start_header_id|>{role}<|end_header_id|>\n\n{content}<|eot_id|>"
        formatted += "<|start_header_id|>assistant<|end_header_id|>\n\n"
        return formatted

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count (rough approximation)."""
        # Llama uses similar tokenization to GPT
        # Rough estimate: ~4 characters per token
        return len(text) // 4


class LlamaOllamaClient(LlamaClient):
    """Convenience class for Ollama backend."""

    def __init__(self, model: str = "llama3.1:8b"):
        super().__init__(model=model, backend="ollama")


class LlamaHuggingFaceClient(LlamaClient):
    """Convenience class for HuggingFace backend."""

    def __init__(self, api_key: Optional[str] = None, model: str = "meta-llama/Meta-Llama-3.1-8B-Instruct"):
        super().__init__(model=model, backend="huggingface", api_key=api_key)
