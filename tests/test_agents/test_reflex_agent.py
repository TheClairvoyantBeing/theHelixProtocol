import pytest
import asyncio
from helix.agents.reflex_agent import ReflexAgent

@pytest.mark.asyncio
async def test_reflex_agent_stop():
    agent = ReflexAgent()
    asyncio.create_task(agent.run())
    await asyncio.sleep(0.1)
    await agent.stop()
    assert agent._stop_event.is_set()
