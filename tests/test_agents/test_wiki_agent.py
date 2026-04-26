import pytest
import asyncio
from helix.agents.wiki_agent import WikiAgent
from helix.event_bus import bus, FileProcessed

@pytest.mark.asyncio
async def test_wiki_agent_stop():
    agent = WikiAgent()
    assert not agent._stop_event.is_set()
    await agent.stop()
    assert agent._stop_event.is_set()

@pytest.mark.asyncio
async def test_wiki_agent_receives_event():
    agent = WikiAgent()
    bus.publish(FileProcessed(record={"id": "foo"}))
    await asyncio.sleep(0.01)
    # Stub just logs, so we just verify no crash
