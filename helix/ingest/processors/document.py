"""Document processor for HELIX ingest pipeline (DOCX, XLSX, PPTX)."""

from pathlib import Path
from helix.ingest.processors.base import BaseProcessor, RawContent
import logging

logger = logging.getLogger(__name__)

class DocumentProcessor(BaseProcessor, mime_patterns=["application/vnd.openxmlformats-officedocument"]):
    """Extracts text and metadata from office documents."""

    def can_handle(self, mime_type: str, extension: str) -> bool:
        return "officedocument" in mime_type or extension in [".docx", ".xlsx", ".pptx"]

    async def extract(self, path: Path) -> RawContent:
        """Extract raw content from a document."""
        logger.info(f"Extracting Document: {path}")
        return RawContent(
            text="Stub document text",
            full_text="Stub document full text",
            frames=[],
            audio_path=None,
            metadata={},
            mime_type="application/octet-stream",
            file_path=path
        )
