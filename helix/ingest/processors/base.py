"""
Module: helix/ingest/processors/base.py
Copyright (c) 2026 HELIX. All rights reserved.

Base processor module for HELIX ingest pipeline.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Any
import logging
import json

logger = logging.getLogger(__name__)

@dataclass
class RawContent:
    """Dataclass holding extracted file contents."""
    text: str                    # extracted text, sanitised, max 8000 chars
    full_text: str               # full text, no truncation (for chunking)
    frames: list[Path]           # temp image files (MUST be cleaned up)
    audio_path: Optional[Path]   # temp audio file (MUST be cleaned up)
    metadata: dict[str, Any]     # EXIF, page count, duration, codec, etc.
    mime_type: str
    file_path: Path

class BaseProcessor(ABC):
    """Abstract base class for all file processors."""

    _registry: dict[str, type["BaseProcessor"]] = {}

    def __init_subclass__(cls, mime_patterns: list[str] = [], **kwargs: Any):
        super().__init_subclass__(**kwargs)
        for pattern in mime_patterns:
            BaseProcessor._registry[pattern] = cls

    @abstractmethod
    def can_handle(self, mime_type: str, extension: str) -> bool:
        """Return True if this processor handles this file type."""
        pass

    @abstractmethod
    async def extract(self, path: Path) -> RawContent:
        """Extract raw content. Must clean up all temp files in finally blocks."""
        pass

    async def generate_record(
        self,
        raw: RawContent,
        llm_client: Any,
        config: Any
    ) -> dict[str, Any]:
        """
        Call LLM to generate FileRecord fields.
        Returns validated dict structure.
        """
        prompt = f"""
        You are a file intelligence assistant. Analyse the following file content
        and return ONLY valid JSON — no markdown, no explanation, just the JSON object.

        File name: {raw.file_path.name}
        File type: {raw.mime_type}

        Content excerpt:
        <document_content>
        {raw.text}
        </document_content>

        Return this exact JSON structure:
        {{
          "category": "Primary/Subcategory",
          "tags": ["tag1", "tag2", "tag3"],
          "summary": "1-2 sentence description, max 200 chars",
          "confidence": 0.85
        }}
        """
        system_prompt = "Return ONLY valid JSON."
        try:
            response = await llm_client.generate(prompt=prompt, system=system_prompt, expect_json=True)
            import re
            cleaned = re.sub(r'^```json\s*|\s*```$', '', response.strip())
            return json.loads(cleaned)
        except Exception as e:
            logger.error(f"Failed to generate record via LLM: {e}")
            return {
                "category": "Unknown",
                "tags": [],
                "summary": "Processing error or unreadable content.",
                "confidence": 0.0
            }

    async def embed(self, file_id: str, raw: RawContent, vector_store: Any) -> None:
        """Chunk full_text and write embeddings to ChromaDB."""
        if not raw.full_text.strip():
            return

        # Basic chunking by words
        words = raw.full_text.split()
        chunk_size = 1000
        overlap = 100

        chunks = []
        step = chunk_size - overlap
        for i in range(0, len(words), step):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)

        # Limit to first 50 chunks for safety
        chunks = chunks[:50]

        if not chunks:
            return

        from helix.llm_client import llm_client
        try:
            embeddings = await llm_client.embed(chunks)
            if embeddings:
                ids = [f"{file_id}_{i:04d}" for i in range(len(chunks))]
                metadatas = [{"file_id": file_id, "chunk_index": i, "file_name": raw.file_path.name} for i in range(len(chunks))]
                vector_store.add_embeddings("helix_chunks", embeddings, chunks, metadatas, ids)
        except Exception as e:
            logger.error(f"Failed to embed chunks: {e}")
