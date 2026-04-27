# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
"""MemoryManager controls working, episodic, and semantic memory."""

import asyncio
import logging
from typing import Any
import json
from datetime import datetime, timezone
from pathlib import Path
from helix.config import config
from helix.event_bus import bus, ChatTurn
from helix.db.schema import get_session
from sqlalchemy import text

logger = logging.getLogger(__name__)

class MemoryManager:
    """Agent that handles memory tiers and consolidation."""

    def __init__(self) -> None:
        self._stop_event = asyncio.Event()
        self._tasks: list[asyncio.Task[Any]] = []

        # Setup memory directories
        self.working_dir = Path(config.vault.index_path).expanduser() / "memory" / "working"
        self.episodic_dir = Path(config.vault.index_path).expanduser() / "memory" / "episodic"
        self.semantic_dir = Path(config.vault.index_path).expanduser() / "memory" / "semantic"

        for d in [self.working_dir, self.episodic_dir, self.semantic_dir]:
            d.mkdir(parents=True, exist_ok=True)

        bus.subscribe(ChatTurn, self._on_chat_turn)

    async def _on_chat_turn(self, event: ChatTurn) -> None:
        """Saves a chat turn into the episodic memory log."""
        try:
            today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            log_path = self.episodic_dir / f"{today_str}.jsonl"

            turn_data = {
                "session_id": event.session_id,
                "turn_index": event.turn_index,
                "role": event.role,
                "content": event.content,
                "timestamp": event.timestamp,
            }

            # Write to episodic file log
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(turn_data) + "\n")

            # Write to database (conversations table)
            async with get_session() as session:
                await session.execute(
                    text("""
                        INSERT INTO conversations (id, session_id, turn_index, role, content, timestamp, memory_tier)
                        VALUES (:id, :session_id, :turn_index, :role, :content, :timestamp, :memory_tier)
                    """),
                    {
                        "id": event.event_id,
                        "session_id": event.session_id,
                        "turn_index": event.turn_index,
                        "role": event.role,
                        "content": event.content,
                        "timestamp": event.timestamp,
                        "memory_tier": "episodic"
                    }
                )
                await session.commit()

            logger.debug(f"MemoryManager saved chat turn for session {event.session_id}")
        except Exception as e:
            logger.error(f"Failed to save episodic memory: {e}")

    async def run(self) -> None:
        while not self._stop_event.is_set():
            # In a full implementation, this would trigger nightly consolidation
            await asyncio.sleep(1.0)

    async def stop(self) -> None:
        self._stop_event.set()
        if self._tasks:
            await asyncio.wait(self._tasks, timeout=30.0)
        logger.info("MemoryManager stopped.")
