# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
"""CalendarAgent manages calendar events and scheduling."""

import asyncio
import logging
from typing import Any
from datetime import datetime, timezone

from sqlalchemy import text
from helix.db.schema import get_session

logger = logging.getLogger(__name__)

class CalendarAgent:
    """Agent that handles calendar events."""

    def __init__(self) -> None:
        self._stop_event = asyncio.Event()
        self._tasks: list[asyncio.Task[Any]] = []

    async def _check_upcoming_events(self) -> None:
        """Polls SQLite for calendar events starting in the next 15 minutes."""
        now = datetime.now(timezone.utc)
        now_str = now.isoformat()

        # Next 15 minutes logic:
        # For simplicity, we just trigger events that are exactly 15 minutes away
        # But for the stub logic, we'll just query events greater than now.
        try:
            async with get_session() as session:
                result = await session.execute(
                    text("SELECT title, start_dt FROM calendar_events WHERE start_dt > :now ORDER BY start_dt ASC LIMIT 1"),
                    {"now": now_str}
                )
                row = result.fetchone()
                if row:
                    title, start_dt = row
                    # Optional: Emits a SystemAlert about the upcoming event if desired
                    # bus.publish(SystemAlert(level="info", message=f"Upcoming Event: {title} at {start_dt}"))
        except Exception as e:
            logger.error(f"CalendarAgent error checking events: {e}")

    async def run(self) -> None:
        """Runs the background checking loop."""
        while not self._stop_event.is_set():
            await self._check_upcoming_events()
            await asyncio.sleep(60.0)

    async def stop(self) -> None:
        self._stop_event.set()
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)
        logger.info("CalendarAgent stopped.")
