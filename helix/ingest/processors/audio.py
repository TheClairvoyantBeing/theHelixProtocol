"""Audio processor for HELIX ingest pipeline."""

from pathlib import Path
from helix.ingest.processors.base import BaseProcessor, RawContent
import logging

logger = logging.getLogger(__name__)

class AudioProcessor(BaseProcessor, mime_patterns=["audio/*"]):
    """Extracts text transcripts and metadata from audio files."""

    def can_handle(self, mime_type: str, extension: str) -> bool:
        return mime_type.startswith("audio/")

    async def extract(self, path: Path) -> RawContent:
        """Extract raw content from an audio file."""
        logger.info(f"Extracting Audio: {path}")
        return RawContent(
            text="Stub audio text",
            full_text="Stub audio full text",
            frames=[],
            audio_path=None,
            metadata={},
            mime_type="audio/mpeg",
            file_path=path
        )
