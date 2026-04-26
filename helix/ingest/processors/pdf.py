"""PDF processor for HELIX ingest pipeline."""

from pathlib import Path
from helix.ingest.processors.base import BaseProcessor, RawContent
import logging

logger = logging.getLogger(__name__)

class PDFProcessor(BaseProcessor, mime_patterns=["application/pdf"]):
    """Extracts text and metadata from PDF files."""

    def can_handle(self, mime_type: str, extension: str) -> bool:
        return mime_type == "application/pdf" or extension == ".pdf"

    async def extract(self, path: Path) -> RawContent:
        """Extract raw content from a PDF."""
        logger.info(f"Extracting PDF: {path}")
        return RawContent(
            text="Stub PDF text",
            full_text="Stub PDF full text",
            frames=[],
            audio_path=None,
            metadata={},
            mime_type="application/pdf",
            file_path=path
        )
