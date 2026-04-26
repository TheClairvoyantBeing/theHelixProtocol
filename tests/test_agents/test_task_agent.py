import pytest
import asyncio
from helix.agents.task_agent import TaskAgent

@pytest.mark.asyncio
async def test_task_agent_stop():
    agent = TaskAgent()
    await agent.stop()
    assert agent._stop_event.is_set()
