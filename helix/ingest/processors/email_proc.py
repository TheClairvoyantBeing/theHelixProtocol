# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
"""Email processor for HELIX ingest pipeline."""

from pathlib import Path
from helix.ingest.processors.base import BaseProcessor, RawContent
import logging

logger = logging.getLogger(__name__)

class EmailProcessor(BaseProcessor, mime_patterns=["message/rfc822", "application/vnd.ms-outlook"]):
    """Extracts text and metadata from email files."""

    def can_handle(self, mime_type: str, extension: str) -> bool:
        return mime_type in ["message/rfc822", "application/vnd.ms-outlook"]

    async def extract(self, path: Path) -> RawContent:
        """Extract raw content from an email."""
        logger.info(f"Extracting Email: {path}")
        return RawContent(
            text="Stub email text",
            full_text="Stub email full text",
            frames=[],
            audio_path=None,
            metadata={},
            mime_type="message/rfc822",
            file_path=path
        )
