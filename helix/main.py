# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
"""
Main entrypoint and orchestrator for HELIX OS.
Handles startup/shutdown sequences and runs the FastAPI server.
"""

import asyncio
import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing import Any

# Force load of config before other imports
from helix.config import config
from helix.hardware import HardwareProbe
from helix.model_selector import ModelSelector
from helix.db.schema import engine, apply_pending_migrations
from helix.event_bus import bus, SystemAlert

from helix.agents.memory_manager import MemoryManager
from helix.agents.wiki_agent import WikiAgent
from helix.agents.graph_builder import GraphBuilder
from helix.agents.task_agent import TaskAgent
from helix.agents.calendar_agent import CalendarAgent
from helix.agents.reflex_agent import ReflexAgent
# Fix Critical Issue 5: import shared chat_engine
from helix.agents.chat_engine import chat_engine as shared_chat_engine
from helix.agents.export_agent import ExportAgent

from helix.ingest.router import FileRouter
from helix.ingest.queue import IngestionQueue
from helix.ingest.watcher import FileWatcher
from helix.scheduler import Scheduler
from helix.voice.voice_gate import VoiceGate
from helix.api.app import app

# Set up logging based on config
logging.basicConfig(
    level=logging.DEBUG if config.vault.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("helix.main")

class HelixOS:
    """Master orchestrator for HELIX components."""

    def __init__(self) -> None:
        self.memory_manager = MemoryManager()
        self.wiki_agent = WikiAgent()
        self.graph_builder = GraphBuilder()
        self.task_agent = TaskAgent()
        self.calendar_agent = CalendarAgent()
        self.reflex_agent = ReflexAgent()
        self.chat_engine = shared_chat_engine
        self.export_agent = ExportAgent()

        self.file_router = FileRouter()
        self.ingestion_queue = IngestionQueue(self.file_router)
        self.file_watcher = FileWatcher()
        self.scheduler = Scheduler()
        self.voice_gate = VoiceGate()
        self.hardware_probe = HardwareProbe()
        self.model_selector = ModelSelector()
        self._tasks: list[asyncio.Task[Any]] = []

    async def start(self) -> None:
        """Start all components in the strict order required by ARCHITECTURE.md."""
        logger.info("Starting HELIX OS...")

        # 1. Hardware Probe
        profile = self.hardware_probe.run()
        logger.info(f"Hardware Profile: Tier {profile.tier} ({profile.gpu_name})")

        # 2. Model Selector
        self.model_selector.select(profile)

        # 3. DB Migrations
        async with engine.begin() as conn:
            await apply_pending_migrations(conn)

        # 4. Start Agents
        agent_tasks: list[Any] = [
            self.memory_manager, self.wiki_agent, self.graph_builder,
            self.task_agent, self.calendar_agent, self.reflex_agent,
            self.chat_engine, self.export_agent
        ]
        for agent in agent_tasks:
            # We don't await the run() as it's an infinite loop, we create a task
            self._tasks.append(asyncio.create_task(agent.run()))

        # 5. Start Pipeline
        await self.ingestion_queue.start()
        await self.file_watcher.start()

        # 6. Start Background Services
        await self.scheduler.start()
        await self.voice_gate.start()

        bus.publish(SystemAlert(level="info", message="HELIX ready"))
        logger.info("HELIX OS Startup Complete.")

    async def stop(self) -> None:
        """Graceful shutdown in reverse order."""
        logger.info("Shutting down HELIX OS...")
        bus.publish(SystemAlert(level="info", message="HELIX shutting down"))

        await self.voice_gate.stop()
        await self.scheduler.stop()

        await self.file_watcher.stop()
        await self.ingestion_queue.stop()

        agent_tasks: list[Any] = [
            self.export_agent, self.chat_engine, self.reflex_agent,
            self.calendar_agent, self.task_agent, self.graph_builder,
            self.wiki_agent, self.memory_manager
        ]
        for agent in agent_tasks:
            await agent.stop()

        await engine.dispose()
        logger.info("Shutdown complete.")

# Global instance
helix_os = HelixOS()

@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    """FastAPI lifespan manager for tying OS lifecycle to the web server."""
    await helix_os.start()
    yield
    await helix_os.stop()

# Attach lifespan to imported app
app.router.lifespan_context = lifespan

def main() -> None:
    """Main entrypoint for running the uvicorn server."""
    logger.info("Initializing application...")

    # Use the 'app' module variable instead of string for PyInstaller compatibility
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=config.ui.port,
        log_level="debug" if config.vault.debug else "info"
    )

if __name__ == "__main__":
    main()
