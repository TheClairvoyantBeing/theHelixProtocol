# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
import pytest
import asyncio
from helix.agents.export_agent import ExportAgent

@pytest.mark.asyncio
async def test_export_agent_stop():
    agent = ExportAgent()
    await agent.stop()
    assert agent._stop_event.is_set()
