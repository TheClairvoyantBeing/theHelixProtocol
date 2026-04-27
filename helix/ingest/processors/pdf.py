# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
"""PDF processor for HELIX ingest pipeline."""

from pathlib import Path
from helix.ingest.processors.base import BaseProcessor, RawContent
import logging
import pdfplumber

logger = logging.getLogger(__name__)

class PDFProcessor(BaseProcessor, mime_patterns=["application/pdf"]):
    """Extracts text and metadata from PDF files."""

    def can_handle(self, mime_type: str, extension: str) -> bool:
        return mime_type == "application/pdf" or extension == ".pdf"

    async def extract(self, path: Path) -> RawContent:
        """Extract raw content from a PDF."""
        logger.info(f"Extracting PDF: {path}")
        text_content = ""
        try:
            with pdfplumber.open(path) as pdf:
                num_pages = min(len(pdf.pages), 50)
                for i in range(num_pages):
                    page = pdf.pages[i]
                    extracted = page.extract_text()
                    if extracted:
                        text_content += extracted + "\n"
        except Exception as e:
            text_content = f"Error extracting PDF: {str(e)}"

        full_text = text_content
        truncated_text = text_content[:8000]

        return RawContent(
            text=truncated_text,
            full_text=full_text,
            frames=[],
            audio_path=None,
            metadata={"source": "PDFProcessor"},
            mime_type="application/pdf",
            file_path=path
        )
