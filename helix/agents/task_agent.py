"""TaskAgent manages tasks and reminders."""

import asyncio
import logging
from typing import Any
from helix.event_bus import bus, TaskCreated
from helix.config import config

logger = logging.getLogger(__name__)

class TaskAgent:
    """Agent that handles task creation, updates, and reminders."""

    def __init__(self) -> None:
        self._stop_event = asyncio.Event()
        self._tasks: list[asyncio.Task[Any]] = []
        bus.subscribe(TaskCreated, self._on_task_created)

    def _on_task_created(self, event: TaskCreated) -> None:
        logger.debug("TaskAgent received TaskCreated event.")

    async def _check_reminders(self) -> None:
        """Periodically checks for due reminders and emits ReminderDue."""
        # Stub implementation
        pass

    async def run(self) -> None:
        while not self._stop_event.is_set():
            await self._check_reminders()
            await asyncio.sleep(config.scheduler.reminder_poll_interval_seconds)

    async def stop(self) -> None:
        self._stop_event.set()
        if self._tasks:
            await asyncio.wait(self._tasks, timeout=30.0)
        logger.info("TaskAgent stopped.")
