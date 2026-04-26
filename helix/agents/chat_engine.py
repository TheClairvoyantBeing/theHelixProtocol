# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
"""ChatEngine agent handles the conversational loop and querying."""

import asyncio
import logging
from typing import Any
from helix.event_bus import bus, ChatTurn

logger = logging.getLogger(__name__)

class ChatEngine:
    """Agent handling user queries and conversation."""

    def __init__(self) -> None:
        self._stop_event = asyncio.Event()
        self._tasks: list[asyncio.Task[Any]] = []
        bus.subscribe(ChatTurn, self._on_chat_turn)

    def _on_chat_turn(self, event: ChatTurn) -> None:
        logger.debug(f"ChatEngine processing ChatTurn for session {event.session_id}")

    async def search(self, query: str, mode: str = "hybrid", limit: int = 10) -> list[dict[str, Any]]:
        """Stub for semantic/hybrid search method."""
        logger.debug(f"ChatEngine search: query='{query}' mode='{mode}'")
        return []

    async def generate_response(self, session_id: str, content: str) -> str:
        """Generates a response for a given session and query."""
        logger.info(f"Generating response for {session_id}")
        return "Stub response"

    async def run(self) -> None:
        while not self._stop_event.is_set():
            await asyncio.sleep(1.0)

    async def stop(self) -> None:
        self._stop_event.set()
        if self._tasks:
            await asyncio.wait(self._tasks, timeout=30.0)
        logger.info("ChatEngine stopped.")
