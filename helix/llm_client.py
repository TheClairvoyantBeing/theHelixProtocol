# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
"""LLM Client for interacting with local models (Ollama/LM Studio)."""

import logging
import httpx
import json
from typing import AsyncGenerator
from pathlib import Path
from helix.config import config

logger = logging.getLogger(__name__)

class LLMClient:
    """Client for generating text and embeddings via local LLMs."""

    def __init__(self):
        self.base_url = config.model.ollama_base
        self.client = httpx.AsyncClient(timeout=120.0)

    async def generate(
        self,
        prompt: str,
        system: str = "",
        model: str | None = None,
        max_tokens: int = 1000,
        timeout: float = 120.0,
        expect_json: bool = False,
    ) -> str:
        """Text generation. Returns response string."""
        model_name = model or config.model.text_model or "llama3"
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model_name,
            "prompt": prompt,
            "system": system,
            "stream": False,
            "options": {
                "num_predict": max_tokens
            }
        }
        if expect_json:
            payload["format"] = "json"

        try:
            response = await self.client.post(url, json=payload, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise

    async def generate_stream(
        self,
        prompt: str,
        system: str = "",
        model: str | None = None,
        timeout: float = 120.0,
    ) -> AsyncGenerator[str, None]:
        """Streaming generation. Yields text chunks."""
        model_name = model or config.model.text_model or "llama3"
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model_name,
            "prompt": prompt,
            "system": system,
            "stream": True,
        }
        try:
            async with self.client.stream("POST", url, json=payload, timeout=timeout) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            if "response" in data:
                                yield data["response"]
                        except json.JSONDecodeError:
                            pass
        except Exception as e:
            logger.error(f"LLM stream generation failed: {e}")
            raise

    async def vision(
        self,
        prompt: str,
        image_path: Path,
        model: str | None = None,
        timeout: float = 120.0,
    ) -> str:
        """Vision/multimodal generation."""
        import base64
        model_name = model or config.model.vision_model or "llava"

        try:
            with open(image_path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode("utf-8")
        except Exception as e:
            logger.error(f"Failed to read image for vision LLM: {e}")
            raise

        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "images": [img_data]
        }
        try:
            response = await self.client.post(url, json=payload, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except Exception as e:
            logger.error(f"Vision LLM generation failed: {e}")
            raise

    async def embed(
        self,
        texts: list[str],
        model: str | None = None,
    ) -> list[list[float]]:
        """Return embeddings for list of texts."""
        model_name = model or config.model.embed_model or "nomic-embed-text"
        url = f"{self.base_url}/api/embed" # Note: Ollama recently added /api/embed, or /api/embeddings.
        # Handling the /api/embeddings vs /api/embed API change in Ollama
        payload = {
            "model": model_name,
            "input": texts
        }
        try:
            response = await self.client.post(url, json=payload, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            # Depending on ollama version it might return 'embeddings' (list of lists) or need singular calls
            if "embeddings" in data:
                return data["embeddings"]
            elif "embedding" in data:
                return [data["embedding"]]
            return []
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                # Fallback to old /api/embeddings endpoint (one at a time)
                url_old = f"{self.base_url}/api/embeddings"
                results = []
                for text in texts:
                    payload_old = {"model": model_name, "prompt": text}
                    resp_old = await self.client.post(url_old, json=payload_old, timeout=30.0)
                    resp_old.raise_for_status()
                    data_old = resp_old.json()
                    results.append(data_old.get("embedding", []))
                return results
            logger.error(f"LLM embedding failed: {e}")
            raise
        except Exception as e:
            logger.error(f"LLM embedding failed: {e}")
            raise

    async def health_check(self) -> bool:
        """Returns True if backend is reachable."""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags", timeout=5.0)
            return response.status_code == 200
        except Exception:
            return False

llm_client = LLMClient()
