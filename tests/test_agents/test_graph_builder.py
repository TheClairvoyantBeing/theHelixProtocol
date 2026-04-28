import pytest
import asyncio
from helix.agents.graph_builder import GraphBuilder
from helix.event_bus import bus, FileProcessed, WikiUpdated
from helix.db.schema import get_session
from sqlalchemy import text

@pytest.mark.asyncio
async def test_graph_builder_wiki_updated():
    builder = GraphBuilder()

    event = WikiUpdated(page_path="/tmp/wiki/Test_Page.md", operation="created")
    bus.publish(event)

    await asyncio.sleep(0.1)

    async with get_session() as session:
        result = await session.execute(text("SELECT label FROM graph_nodes WHERE label = 'Test_Page'"))
        row = result.fetchone()
        assert row is not None
