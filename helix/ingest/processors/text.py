"""Text processor for HELIX ingest pipeline."""

from pathlib import Path
from helix.ingest.processors.base import BaseProcessor, RawContent
import logging

logger = logging.getLogger(__name__)

class TextProcessor(BaseProcessor, mime_patterns=["text/plain", "text/csv", "application/json", "text/x-python"]):
    """Extracts text from plain text files and code."""

    def can_handle(self, mime_type: str, extension: str) -> bool:
        return mime_type.startswith("text/") or mime_type in ["application/json", "application/x-yaml"]

    async def extract(self, path: Path) -> RawContent:
        """Extract raw content from a text file."""
        logger.info(f"Extracting Text: {path}")
        return RawContent(
            text="Stub text",
            full_text="Stub full text",
            frames=[],
            audio_path=None,
            metadata={},
            mime_type="text/plain",
            file_path=path
        )
