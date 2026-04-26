# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
"""ExportAgent manages exporting data to encrypted archives."""

import asyncio
import logging
from typing import Any

logger = logging.getLogger(__name__)

class ExportAgent:
    """Agent that creates encrypted export packages."""

    def __init__(self) -> None:
        self._stop_event = asyncio.Event()
        self._tasks: list[asyncio.Task[Any]] = []

    async def run(self) -> None:
        while not self._stop_event.is_set():
            await asyncio.sleep(1.0)

    async def stop(self) -> None:
        self._stop_event.set()
        if self._tasks:
            await asyncio.wait(self._tasks, timeout=30.0)
        logger.info("ExportAgent stopped.")
