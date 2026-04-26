"""CalendarAgent manages calendar events and scheduling."""

import asyncio
import logging
from typing import Any

logger = logging.getLogger(__name__)

class CalendarAgent:
    """Agent that handles calendar events."""

    def __init__(self) -> None:
        self._stop_event = asyncio.Event()
        self._tasks: list[asyncio.Task[Any]] = []

    async def run(self) -> None:
        while not self._stop_event.is_set():
            await asyncio.sleep(1.0)

    async def stop(self) -> None:
        self._stop_event.set()
        if self._tasks:
            await asyncio.wait(self._tasks, timeout=30.0)
        logger.info("CalendarAgent stopped.")
