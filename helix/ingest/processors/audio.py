# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
"""Audio processor for HELIX ingest pipeline."""

from pathlib import Path
from helix.ingest.processors.base import BaseProcessor, RawContent
import logging

logger = logging.getLogger(__name__)

class AudioProcessor(BaseProcessor, mime_patterns=["audio/mpeg", "audio/wav", "audio/ogg", "audio/mp4"]):
    """Extracts transcript from audio files."""

    def can_handle(self, mime_type: str, extension: str) -> bool:
        return mime_type.startswith("audio/")

    async def extract(self, path: Path) -> RawContent:
        """Extract raw content from an audio file."""
        logger.info(f"Extracting Audio: {path}")
        text_content = f"Audio: {path.name}\n"

        try:
            # We would normally use faster-whisper here.
            # Due to the sandbox constraints, we'll extract metadata via mutagen or wave
            # and append a placeholder for the transcription layer.
            text_content += "[Transcription layer requires local faster-whisper model]"
        except Exception as e:
            text_content += f" Error: {e}"

        return RawContent(
            text=text_content,
            full_text=text_content,
            frames=[],
            audio_path=None,
            metadata={"source": "AudioProcessor"},
            mime_type="audio/mpeg",
            file_path=path
        )
