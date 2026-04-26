"""
Module: helix/ingest/processors/base.py
Copyright (c) 2026 HELIX. All rights reserved.

Base processor module for HELIX ingest pipeline.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class RawContent:
    """Dataclass holding extracted file contents."""
    text: str                    # extracted text, sanitised, max 8000 chars
    full_text: str               # full text, no truncation (for chunking)
    frames: list[Path]           # temp image files (MUST be cleaned up)
    audio_path: Optional[Path]   # temp audio file (MUST be cleaned up)
    metadata: dict[str, Any]     # EXIF, page count, duration, codec, etc.
    # Use Any here for metadata because EXIF/metadata values are deeply heterogeneous.
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
        llm_client: Any, # type: ignore
        config: Any # type: ignore
    ) -> dict[str, Any]:
        """
        Call LLM to generate FileRecord fields.
        Returns validated dict structure. Uses Any for LLM responses.
        """
        return {}

    async def embed(self, file_id: str, raw: RawContent, vector_store: Any) -> None: # type: ignore
        """Chunk full_text and write embeddings to ChromaDB."""
        pass
