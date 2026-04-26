"""
Module: helix/agents/task_agent.py
Copyright (c) 2026 HELIX. All rights reserved.

TaskAgent manages the lifecycle of user tasks and emits reminders.
"""

import asyncio
import logging
from typing import Any
from sqlalchemy import text
from datetime import datetime, timezone

from helix.event_bus import bus, TaskCreated, ReminderDue
from helix.config import config
from helix.db.schema import get_session

logger = logging.getLogger(__name__)

class TaskAgent:
    """
    Agent that handles task creation, updates, and reminders.
    Monitors databases to trigger reminder events when due.
    """

    def __init__(self) -> None:
        self._stop_event = asyncio.Event()
        self._tasks: list[asyncio.Task[Any]] = []
        bus.subscribe(TaskCreated, self._on_task_created)

    def _on_task_created(self, event: TaskCreated) -> None:
        logger.debug("TaskAgent received TaskCreated event.")

    async def _check_reminders(self) -> None:
        now_str = datetime.now(timezone.utc).isoformat()
        try:
            async with get_session() as session:
                result = await session.execute(
                    text("SELECT id, task_id, message FROM reminders WHERE remind_at <= :now AND delivered = 0"),
                    {"now": now_str}
                )
                rows = result.fetchall()
                for row in rows:
                    reminder_data = {"id": row[0], "task_id": row[1], "message": row[2]}
                    bus.publish(ReminderDue(reminder=reminder_data))
                    await session.execute(
                        text("UPDATE reminders SET delivered = 1 WHERE id = :id"),
                        {"id": row[0]}
                    )
                await session.commit()
        except Exception as e:
            logger.error(f"Error checking reminders: {e}")

    async def run(self) -> None:
        while not self._stop_event.is_set():
            await self._check_reminders()
            await asyncio.sleep(config.scheduler.reminder_poll_interval_seconds)

    async def stop(self) -> None:
        self._stop_event.set()
        if self._tasks:
            await asyncio.wait(self._tasks, timeout=30.0)
        logger.info("TaskAgent stopped.")
