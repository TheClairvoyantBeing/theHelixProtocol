# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
"""
Processor registry initializer.
Imports all processor modules to ensure __init_subclass__ triggers registration.
"""

from .audio import AudioProcessor
from .document import DocumentProcessor
from .email_proc import EmailProcessor
from .image import ImageProcessor
from .pdf import PDFProcessor
from .text import TextProcessor
from .video import VideoProcessor

__all__ = [
    "AudioProcessor",
    "DocumentProcessor",
    "EmailProcessor",
    "ImageProcessor",
    "PDFProcessor",
    "TextProcessor",
    "VideoProcessor"
]
