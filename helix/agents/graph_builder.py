"""GraphBuilder agent constructs the knowledge graph."""

import asyncio
import logging
from typing import Any
from helix.event_bus import bus, FileProcessed, WikiUpdated

logger = logging.getLogger(__name__)

class GraphBuilder:
    """Agent that curates the graph nodes and edges."""

    def __init__(self) -> None:
        self._stop_event = asyncio.Event()
        self._tasks: list[asyncio.Task[Any]] = []
        bus.subscribe(FileProcessed, self._on_file_processed)
        bus.subscribe(WikiUpdated, self._on_wiki_updated)

    def _on_file_processed(self, event: FileProcessed) -> None:
        logger.debug("GraphBuilder processing FileProcessed event.")

    def _on_wiki_updated(self, event: WikiUpdated) -> None:
        logger.debug("GraphBuilder processing WikiUpdated event.")

    async def run(self) -> None:
        while not self._stop_event.is_set():
            await asyncio.sleep(1.0)

    async def stop(self) -> None:
        self._stop_event.set()
        if self._tasks:
            await asyncio.wait(self._tasks, timeout=30.0)
        logger.info("GraphBuilder stopped.")
