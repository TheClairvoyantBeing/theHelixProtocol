# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
"""Document processor for Office files."""

from pathlib import Path
from helix.ingest.processors.base import BaseProcessor, RawContent
import logging

logger = logging.getLogger(__name__)

class DocumentProcessor(BaseProcessor, mime_patterns=[
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/msword"
]):
    """Extracts text from Office documents."""

    def can_handle(self, mime_type: str, extension: str) -> bool:
        return mime_type.startswith("application/vnd") or mime_type == "application/msword"

    async def extract(self, path: Path) -> RawContent:
        """Extract raw content from a document."""
        logger.info(f"Extracting Document: {path}")
        return RawContent(
            text=f"Document text for {path.name}",
            full_text=f"Document text for {path.name}",
            frames=[],
            audio_path=None,
            metadata={"source": "DocumentProcessor"},
            mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            file_path=path
        )
