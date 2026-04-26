# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
import pytest
import asyncio
from helix.agents.memory_manager import MemoryManager

@pytest.mark.asyncio
async def test_memory_manager_stop():
    agent = MemoryManager()
    await agent.stop()
    assert agent._stop_event.is_set()
