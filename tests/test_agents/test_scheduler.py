"""
Module: tests/test_agents/test_scheduler.py
Copyright (c) 2026 HELIX. All rights reserved.

Test scheduler.
"""
import pytest
from helix.scheduler import Scheduler

@pytest.mark.asyncio
async def test_scheduler_stop():
    agent = Scheduler()
    await agent.stop()
    assert agent._running is False
