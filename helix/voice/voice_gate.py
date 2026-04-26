"""VoiceGate handles wake word and microphone capture."""

import asyncio
import logging
from typing import Any
from helix.config import config

logger = logging.getLogger(__name__)

class VoiceGate:
    """Manages voice capture and processing."""

    def __init__(self) -> None:
        self._running = False
        self._task: asyncio.Task[Any] | None = None

    async def start(self) -> None:
        if not config.voice.enabled:
            return
        self._running = True
        self._task = asyncio.create_task(self._listen_loop())
        logger.info("VoiceGate started.")

    async def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("VoiceGate stopped.")

    async def _listen_loop(self) -> None:
        while self._running:
            await asyncio.sleep(5.0)
