"""
Module: helix/ingest/watcher.py
Copyright (c) 2026 HELIX. All rights reserved.

File watcher module to emit FileQueued events.
"""

import asyncio
import hashlib
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
        """
        Polls configured vault directories for new files.
        (Placeholder for watchfiles implementation)
        """
        while self._running:
            # Logic to scan config.vault.root_dirs
            # Identify modified files and queue them via queue_file
            await asyncio.sleep(5.0)

    def queue_file(self, file_path: Path) -> None:
        """Manually queues a file for testing/one-off ingestion."""
        if not file_path.exists() or not file_path.is_file():
            return

        try:
            # ALWAYS use python-magic to get accurate MIME type (Rule from DO_NOT_DO.md)
            mime_type = magic.from_file(str(file_path), mime=True)

            # Compute SHA-256 hash for file deduplication
            sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    sha256.update(chunk)
            file_hash = sha256.hexdigest()

            event = FileQueued(path=str(file_path), file_hash=file_hash, mime_type=mime_type)
            bus.publish(event)
        except Exception as e:
            logger.error(f"Error queueing file {file_path}: {e}")
