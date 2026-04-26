"""Routes files to the appropriate processor based on MIME type."""

from typing import Type
import logging
from helix.ingest.processors.base import BaseProcessor

logger = logging.getLogger(__name__)

class FileRouter:
    """Determines the appropriate processor for a given file."""

    def get_processor(self, mime_type: str, extension: str) -> Type[BaseProcessor] | None:
        """Returns the processor class for the given MIME type and extension."""
        # Try exact MIME match
        for pattern, processor_cls in BaseProcessor._registry.items():
            if mime_type.startswith(pattern.replace("/*", "")):
                # Just a basic routing rule, we'll instantiate it
                return processor_cls

        # Fallback to checking can_handle manually on all registered processors
        for processor_cls in set(BaseProcessor._registry.values()):
            # Instantiate temporarily to check or make can_handle a classmethod
            # Let's assume we can instantiate without args for now, or just use class logic
            try:
                processor = processor_cls()
                if processor.can_handle(mime_type, extension):
                    return processor_cls
            except Exception:
                pass

        return None
