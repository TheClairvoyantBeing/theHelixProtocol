"""Scheduler for recurring background jobs."""

import asyncio
import logging
from typing import Any

logger = logging.getLogger(__name__)

class Scheduler:
    """Manages scheduled background tasks like consolidation and reflection."""

    def __init__(self) -> None:
        self._running = False
        self._task: asyncio.Task[Any] | None = None

    async def start(self) -> None:
        self._running = True
        self._task = asyncio.create_task(self._loop())
        logger.info("Scheduler started.")

    async def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Scheduler stopped.")

    async def _loop(self) -> None:
        # Simple sleep loop for the stub
        while self._running:
            await asyncio.sleep(60.0)
