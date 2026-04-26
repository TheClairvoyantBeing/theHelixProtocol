"""
Module: helix/ingest/queue.py
Copyright (c) 2026 HELIX. All rights reserved.

Manages the queue of files waiting to be processed.
"""

import asyncio
from pathlib import Path
from typing import Any
import logging
from helix.event_bus import bus, FileQueued
from helix.ingest.router import FileRouter
from helix.config import config

logger = logging.getLogger(__name__)

class IngestionQueue:
    """Queue system for managing file ingestion workloads."""

    def __init__(self, router: FileRouter) -> None:
        self.router = router
        self.queue: asyncio.Queue[FileQueued] = asyncio.Queue()
        self._workers: list[asyncio.Task[Any]] = []
        self._running = False

        bus.subscribe(FileQueued, self._on_file_queued)

    def _on_file_queued(self, event: FileQueued) -> None:
        """Handler for FileQueued events."""
        if self._running:
            self.queue.put_nowait(event)
            logger.debug(f"Queued file: {event.path}")

    async def start(self) -> None:
        self._running = True
        num_workers = config.processing.max_workers
        for i in range(num_workers):
            task = asyncio.create_task(self._worker(i))
            self._workers.append(task)
        logger.info(f"IngestionQueue started with {num_workers} workers.")

    async def stop(self) -> None:
        self._running = False
        for task in self._workers:
            task.cancel()
        if self._workers:
            await asyncio.gather(*self._workers, return_exceptions=True)
        self._workers.clear()
        logger.info("IngestionQueue stopped.")

    async def _worker(self, worker_id: int) -> None:
        """Asynchronous worker that pulls from the queue and processes files."""
        while self._running:
            try:
                event = await self.queue.get()
                await self._process_file(event)
                self.queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Worker {worker_id} error: {e}", exc_info=True)

    async def _process_file(self, event: FileQueued) -> None:
        """Invokes the appropriate processor for the file."""
        path = Path(event.path)
        processor_cls = self.router.get_processor(event.mime_type, path.suffix.lower())
        if not processor_cls:
            logger.warning(f"No processor found for {event.path} ({event.mime_type})")
            return

        logger.info(f"Processing {event.path} with {processor_cls.__name__}")

        processor = processor_cls()
        try:
            # Emulates extraction pipeline
            raw = await processor.extract(path)
            await processor.generate_record(raw, None, config)
            # In a full implementation, the DB upsert and ChromaDB embedding happen here
            logger.info(f"Successfully processed {path.name}")
        except Exception as e:
            logger.error(f"Error processing {path.name}: {e}")
