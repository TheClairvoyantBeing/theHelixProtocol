# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
"""Text processor for HELIX ingest pipeline."""

from pathlib import Path
from helix.ingest.processors.base import BaseProcessor, RawContent
import logging
import aiofiles

logger = logging.getLogger(__name__)

class TextProcessor(BaseProcessor, mime_patterns=["text/plain", "text/csv", "application/json", "text/x-python"]):
    """Extracts text from plain text files and code."""

    def can_handle(self, mime_type: str, extension: str) -> bool:
        return mime_type.startswith("text/") or mime_type in ["application/json", "application/x-yaml"]

    async def extract(self, path: Path) -> RawContent:
        """Extract raw content from a text file."""
        logger.info(f"Extracting Text: {path}")

        text_content = ""
        try:
            async with aiofiles.open(path, mode='r', encoding='utf-8', errors='ignore') as f:
                text_content = await f.read()
        except Exception as e:
            text_content = f"Error extracting Text: {str(e)}"

        full_text = text_content
        truncated_text = text_content[:8000]

        return RawContent(
            text=truncated_text,
            full_text=full_text,
            frames=[],
            audio_path=None,
            metadata={"source": "TextProcessor"},
            mime_type="text/plain",
            file_path=path
        )
