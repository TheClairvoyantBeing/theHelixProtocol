"""
Module: helix/main.py
Copyright (c) 2026 HELIX. All rights reserved.

Single entrypoint for HELIX OS. Orchestrates startup and shutdown sequences.
"""

import asyncio
import logging
from typing import Any
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from helix.config import config
from helix.hardware import HardwareProbe
from helix.model_selector import ModelSelector
from helix.db.schema import engine, apply_pending_migrations
from helix.event_bus import bus, SystemAlert
from helix.scheduler import Scheduler
from helix.voice.voice_gate import VoiceGate
from helix.ingest.watcher import FileWatcher
from helix.ingest.router import FileRouter
from helix.ingest.queue import IngestionQueue

# Agents
from helix.agents.memory_manager import MemoryManager
from helix.agents.wiki_agent import WikiAgent
from helix.agents.graph_builder import GraphBuilder
from helix.agents.task_agent import TaskAgent
from helix.agents.calendar_agent import CalendarAgent
from helix.agents.reflex_agent import ReflexAgent
from helix.agents.chat_engine import ChatEngine
from helix.agents.export_agent import ExportAgent

from helix.api.app import app

logging.basicConfig(level=logging.DEBUG if config.vault.debug else logging.INFO)
logger = logging.getLogger(__name__)

class HelixOS:
    """Manages the full lifecycle of the HELIX OS components."""

    def __init__(self) -> None:
        self.scheduler = Scheduler()
        self.voice_gate = VoiceGate()
        self.router = FileRouter()
        self.queue = IngestionQueue(self.router)
        self.watcher = FileWatcher()

        # Initialize agents
        self.memory_manager = MemoryManager()
        self.wiki_agent = WikiAgent()
        self.graph_builder = GraphBuilder()
        self.task_agent = TaskAgent()
        self.calendar_agent = CalendarAgent()
        self.reflex_agent = ReflexAgent()
        self.chat_engine = ChatEngine()
        self.export_agent = ExportAgent()

        self._tasks: list[asyncio.Task[Any]] = []

    async def startup(self) -> None:
        """Executes the startup sequence from Phase 5.1 of ARCHITECTURE.md."""
        logger.info("Starting HELIX...")

        # 1. Config loaded (happens on import)

        # 2. Hardware Probe
        probe = HardwareProbe()
        profile = probe.run()

        # 3. Model Selector
        selector = ModelSelector()
        selector.select(profile)

        # 4. DB Migrations
        async with engine.begin() as conn:
            await apply_pending_migrations(conn) # type: ignore

        # 5. FastAPI is started by uvicorn below

        # 6 & 7. Start Agents (in specific order)
        agents = [
            self.memory_manager, self.wiki_agent, self.graph_builder,
            self.task_agent, self.calendar_agent, self.reflex_agent,
            self.chat_engine, self.export_agent
        ]
        for agent in agents:
            self._tasks.append(asyncio.create_task(agent.run())) # type: ignore

        # 8. Start Ingestion
        await self.queue.start()
        await self.watcher.start()

        # 9. Start Scheduler
        await self.scheduler.start()

        # 10. Start VoiceGate
        await self.voice_gate.start()

        bus.publish(SystemAlert(level="info", message="HELIX ready"))
        logger.info("HELIX ready.")

    async def shutdown(self) -> None:
        """Executes the shutdown sequence from Phase 5.2 of ARCHITECTURE.md."""
        logger.info("Shutting down HELIX...")
        bus.publish(SystemAlert(level="info", message="HELIX shutting down"))

        await self.watcher.stop()
        await self.voice_gate.stop()
        await self.queue.stop()

        agents = [
            self.export_agent, self.chat_engine, self.reflex_agent,
            self.calendar_agent, self.task_agent, self.graph_builder,
            self.wiki_agent, self.memory_manager
        ]
        for agent in agents:
            await agent.stop() # type: ignore

        for task in self._tasks:
            task.cancel()

        await engine.dispose()
        logger.info("HELIX gracefully stopped.")

helix_os = HelixOS()

@asynccontextmanager
async def lifespan(app: FastAPI) -> Any: # type: ignore
    """Lifespan hook for FastAPI."""
    await helix_os.startup()
    yield
    await helix_os.shutdown()

app.router.lifespan_context = lifespan # type: ignore

def main() -> None:
    """Entry point wrapper for uvicorn."""
    pass # is_dev = "--dev" in sys.argv
    uvicorn.run(app, host="127.0.0.1", port=config.ui.port)

if __name__ == "__main__":
    main()
