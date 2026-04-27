"""
Module: helix/ingest/queue.py
Copyright (c) 2026 HELIX. All rights reserved.

Manages the queue of files waiting to be processed.
"""

import asyncio
from pathlib import Path
from typing import Any
import logging
import uuid
from datetime import datetime, timezone
from sqlalchemy import text

from helix.event_bus import bus, FileQueued, FileProcessed
from helix.ingest.router import FileRouter
from helix.config import config
from helix.db.schema import get_session
from helix.llm_client import llm_client
from helix.db.vector_store import vector_store

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

        # 1. Deduplication Check
        async with get_session() as session:
            result = await session.execute(
                text("SELECT id, status FROM files WHERE file_path = :path AND file_hash = :hash"),
                {"path": str(path), "hash": event.file_hash}
            )
            existing = result.fetchone()
            if existing and existing[1] == "done":
                logger.debug(f"Skipping {path.name}: Unchanged and already processed.")
                return

        # 2. Route to Processor
        processor_cls = self.router.get_processor(event.mime_type, path.suffix.lower())
        if not processor_cls:
            logger.warning(f"No processor found for {event.path} ({event.mime_type})")
            return

        logger.info(f"Processing {event.path} with {processor_cls.__name__}")
        processor = processor_cls()
        file_id = str(uuid.uuid4())

        try:
            # 3. Extract
            raw = await processor.extract(path)

            # 4. Generate Record
            record_dict = await processor.generate_record(raw, llm_client, config)

            # 5. Embed to Vector Store
            await processor.embed(file_id, raw, vector_store)

            # 6. Save to SQLite
            now_str = datetime.now(timezone.utc).isoformat()
            async with get_session() as session:
                await session.execute(
                    text("""
                        INSERT INTO files (id, file_path, file_hash, file_name, extension, mime_type, file_size_kb, indexed_at, status, category)
                        VALUES (:id, :path, :hash, :name, :ext, :mime, :size, :now, 'done', :cat)
                        ON CONFLICT(file_path) DO UPDATE SET
                            file_hash=excluded.file_hash,
                            indexed_at=excluded.indexed_at,
                            status=excluded.status,
                            category=excluded.category
                    """),
                    {
                        "id": file_id,
                        "path": str(path),
                        "hash": event.file_hash,
                        "name": path.name,
                        "ext": path.suffix.lower(),
                        "mime": event.mime_type,
                        "size": path.stat().st_size / 1024,
                        "now": now_str,
                        "cat": record_dict.get("category", "Unknown")
                    }
                )
                await session.commit()

            bus.publish(FileProcessed(record={"id": file_id, "path": str(path), "category": record_dict.get("category", "Unknown")}))
            logger.info(f"Successfully processed {path.name}")

        except Exception as e:
            logger.error(f"Error processing {path.name}: {e}")
            async with get_session() as session:
                await session.execute(
                    text("UPDATE files SET status = 'error', error_msg = :err WHERE file_path = :path"),
                    {"path": str(path), "err": str(e)}
                )
                await session.commit()
