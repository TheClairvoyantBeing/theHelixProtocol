# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
"""Video processor for HELIX ingest pipeline."""

from pathlib import Path
from helix.ingest.processors.base import BaseProcessor, RawContent
import logging

logger = logging.getLogger(__name__)

class VideoProcessor(BaseProcessor, mime_patterns=["video/*"]):
    """Extracts frames, audio, and metadata from video files."""

    def can_handle(self, mime_type: str, extension: str) -> bool:
        return mime_type.startswith("video/")

    async def extract(self, path: Path) -> RawContent:
        """Extract raw content from a video."""
        logger.info(f"Extracting Video: {path}")
        return RawContent(
            text="Stub video text",
            full_text="Stub video full text",
            frames=[],
            audio_path=None,
            metadata={},
            mime_type="video/mp4",
            file_path=path
        )
