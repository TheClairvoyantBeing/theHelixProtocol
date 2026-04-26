"""WikiAgent manages markdown knowledge pages."""

import asyncio
import logging
from typing import Any
from helix.event_bus import bus, FileProcessed

logger = logging.getLogger(__name__)

class WikiAgent:
    """Agent that curates the vault/wiki/ markdown files."""

    def __init__(self) -> None:
        self._stop_event = asyncio.Event()
        self._tasks: list[asyncio.Task[Any]] = []
        bus.subscribe(FileProcessed, self._on_file_processed)

    def _on_file_processed(self, event: FileProcessed) -> None:
        # Just logging for now
        logger.debug(f"WikiAgent received FileProcessed for record: {event.record}")

    async def run(self) -> None:
        """Long-running coroutine."""
        while not self._stop_event.is_set():
            await asyncio.sleep(1.0)

    async def stop(self) -> None:
        """Signal the run loop to exit."""
        self._stop_event.set()
        if self._tasks:
            await asyncio.wait(self._tasks, timeout=30.0)
        logger.info("WikiAgent stopped.")
