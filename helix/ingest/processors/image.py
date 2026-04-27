# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
"""Image processor for extracting metadata and vision analysis from image files."""

from pathlib import Path
from typing import Any
from PIL import Image
import piexif # type: ignore
import logging

from helix.ingest.processors.base import BaseProcessor, RawContent

logger = logging.getLogger(__name__)

class ImageProcessor(BaseProcessor, mime_patterns=["image/jpeg", "image/png", "image/webp", "image/gif"]):
    """Processor for Image files."""

    def can_handle(self, mime_type: str, extension: str) -> bool:
        return mime_type.startswith("image/")

    async def extract(self, path: Path) -> RawContent:
        metadata: dict[str, Any] = {}
        try:
            with Image.open(path) as img:
                metadata["format"] = img.format
                metadata["size"] = img.size
                metadata["mode"] = img.mode

                try:
                    exif_dict = piexif.load(img.info.get('exif', b''))
                    if "0th" in exif_dict and piexif.ImageIFD.Make in exif_dict["0th"]:
                        metadata["make"] = exif_dict["0th"][piexif.ImageIFD.Make].decode('utf-8', 'ignore')
                    if "0th" in exif_dict and piexif.ImageIFD.Model in exif_dict["0th"]:
                        metadata["model"] = exif_dict["0th"][piexif.ImageIFD.Model].decode('utf-8', 'ignore')
                except Exception:
                    pass

        except Exception as e:
            logger.error(f"Error extracting Image metadata: {e}")
            metadata["error"] = str(e)

        return RawContent(
            text="",
            full_text="",
            frames=[],
            audio_path=None,
            metadata=metadata,
            mime_type="image/jpeg",
            file_path=path
        )
