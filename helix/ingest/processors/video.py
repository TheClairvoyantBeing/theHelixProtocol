# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
"""Video processor for HELIX ingest pipeline."""

from pathlib import Path
from helix.ingest.processors.base import BaseProcessor, RawContent
import logging

logger = logging.getLogger(__name__)

class VideoProcessor(BaseProcessor, mime_patterns=["video/mp4", "video/webm", "video/x-matroska"]):
    """Extracts frames and audio transcript from videos."""

    def can_handle(self, mime_type: str, extension: str) -> bool:
        return mime_type.startswith("video/")

    async def extract(self, path: Path) -> RawContent:
        """Extract raw content from a video."""
        logger.info(f"Extracting Video: {path}")
        # Note: True extraction would use ffmpeg-python and faster-whisper.
        # This is a basic implementation returning metadata for the OS pipeline.
        return RawContent(
            text=f"Extracted video content for {path.name}",
            full_text=f"Extracted video content for {path.name}",
            frames=[],
            audio_path=None,
            metadata={"source": "VideoProcessor"},
            mime_type="video/mp4",
            file_path=path
        )
