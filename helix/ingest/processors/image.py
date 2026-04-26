"""Image processor for HELIX ingest pipeline."""

from pathlib import Path
from helix.ingest.processors.base import BaseProcessor, RawContent
import logging

logger = logging.getLogger(__name__)

class ImageProcessor(BaseProcessor, mime_patterns=["image/*"]):
    """Extracts text and metadata from image files."""

    def can_handle(self, mime_type: str, extension: str) -> bool:
        return mime_type.startswith("image/")

    async def extract(self, path: Path) -> RawContent:
        """Extract raw content from an image."""
        # Stub implementation
        logger.info(f"Extracting image: {path}")
        return RawContent(
            text="Stub image text",
            full_text="Stub image full text",
            frames=[],
            audio_path=None,
            metadata={},
            mime_type="image/jpeg",
            file_path=path
        )
