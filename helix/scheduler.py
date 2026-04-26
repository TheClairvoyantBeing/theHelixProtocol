"""
Module: helix/scheduler.py
Copyright (c) 2026 HELIX. All rights reserved.

Scheduler for recurring background jobs.
"""

import asyncio
import logging
from typing import Any
from datetime import datetime, timezone
from helix.config import config

logger = logging.getLogger(__name__)

class Scheduler:
    """Manages scheduled background tasks like consolidation and reflection."""

    def __init__(self) -> None:
        self._running = False
        self._task: asyncio.Task[Any] | None = None
        self._last_consolidation_run = -1

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
        """Main polling loop to trigger nightly jobs based on current time."""
        while self._running:
            now = datetime.now(timezone.utc)

            # Check nightly consolidation hour
            if now.hour == config.scheduler.nightly_consolidation_hour and self._last_consolidation_run != now.day:
                logger.info("Triggering nightly memory consolidation.")
                self._last_consolidation_run = now.day
                # Emit event or call memory manager directly via bus
                # In a full implementation, we might publish an event here

            await asyncio.sleep(60.0)
