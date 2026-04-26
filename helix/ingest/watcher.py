"""File watcher module to emit FileQueued events."""

import asyncio
from pathlib import Path
from typing import Any
import magic
from helix.event_bus import bus, FileQueued
import logging

logger = logging.getLogger(__name__)

class FileWatcher:
    """Watches the vault for new files to index."""
    def __init__(self) -> None:
        self._running = False
        self._task: asyncio.Task[Any] | None = None

    async def start(self) -> None:
        self._running = True
        self._task = asyncio.create_task(self._watch_loop())
        logger.info("FileWatcher started.")

    async def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("FileWatcher stopped.")

    async def _watch_loop(self) -> None:
        # In a real implementation this would use watchfiles.
        # For now, it's a stub loop that just sleeps.
        while self._running:
            await asyncio.sleep(5.0)

    def queue_file(self, file_path: Path) -> None:
        """Manually queues a file for testing/one-off ingestion."""
        if not file_path.exists() or not file_path.is_file():
            return

        try:
            mime_type = magic.from_file(str(file_path), mime=True)
            # Dummy hash for now
            file_hash = "dummyhash"
            event = FileQueued(path=str(file_path), file_hash=file_hash, mime_type=mime_type)
            bus.publish(event)
        except Exception as e:
            logger.error(f"Error queueing file {file_path}: {e}")
