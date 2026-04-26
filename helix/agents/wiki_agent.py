"""
Module: helix/agents/wiki_agent.py
Copyright (c) 2026 HELIX. All rights reserved.

WikiAgent manages markdown knowledge pages in the vault/wiki/ directory.
It responds to FileProcessed events to update the wiki graph.
"""

import asyncio
import logging
from typing import Any
from helix.event_bus import bus, FileProcessed

logger = logging.getLogger(__name__)

class WikiAgent:
    """
    Agent that curates the vault/wiki/ markdown files.
    Listens for FileProcessed events to maintain human-readable knowledge summaries.
    """

    def __init__(self) -> None:
        # Event used to signal the agent to shut down cleanly
        self._stop_event = asyncio.Event()
        # List of active background tasks for the agent
        self._tasks: list[asyncio.Task[Any]] = []

        # Subscribe to new files being fully processed by the ingestion pipeline
        bus.subscribe(FileProcessed, self._on_file_processed)

    def _on_file_processed(self, event: FileProcessed) -> None:
        """
        Handler triggered when a new file has been successfully processed.
        Should extract knowledge and update markdown wiki pages.
        """
        logger.debug(f"WikiAgent received FileProcessed for record: {event.record}")

    async def run(self) -> None:
        """
        Long-running coroutine for the agent's main loop.
        Maintains an active state until the stop event is triggered.
        """
        while not self._stop_event.is_set():
            # Sleep briefly to yield control back to the event loop
            await asyncio.sleep(1.0)

    async def stop(self) -> None:
        """
        Signals the agent's run loop to exit and cleans up background tasks.
        Waits a maximum of 30 seconds for tasks to finish gracefully.
        """
        self._stop_event.set()
        if self._tasks:
            # Wait for all background tasks to finish processing
            await asyncio.wait(self._tasks, timeout=30.0)
        logger.info("WikiAgent stopped.")
