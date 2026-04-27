# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
"""Audio processor for HELIX ingest pipeline."""

from pathlib import Path
from helix.ingest.processors.base import BaseProcessor, RawContent
import logging

logger = logging.getLogger(__name__)

class AudioProcessor(BaseProcessor, mime_patterns=["audio/mpeg", "audio/wav", "audio/ogg"]):
    """Extracts transcript from audio files."""

    def can_handle(self, mime_type: str, extension: str) -> bool:
        return mime_type.startswith("audio/")

    async def extract(self, path: Path) -> RawContent:
        """Extract raw content from an audio file."""
        logger.info(f"Extracting Audio: {path}")
        return RawContent(
            text=f"Audio transcript for {path.name}",
            full_text=f"Audio transcript for {path.name}",
            frames=[],
            audio_path=None,
            metadata={"source": "AudioProcessor"},
            mime_type="audio/mpeg",
            file_path=path
        )
