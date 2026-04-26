import pytest
import asyncio
from helix.ingest.queue import IngestionQueue
from helix.ingest.router import FileRouter
from helix.event_bus import bus, FileQueued

@pytest.mark.asyncio
async def test_queue_start_stop():
    router = FileRouter()
    queue = IngestionQueue(router)
    await queue.start()
    assert queue._running is True
    assert len(queue._workers) > 0
    await queue.stop()
    assert queue._running is False
    assert len(queue._workers) == 0

@pytest.mark.asyncio
async def test_queue_receives_event():
    router = FileRouter()
    queue = IngestionQueue(router)
    queue._running = True

    event = FileQueued(path="/foo.pdf", mime_type="application/pdf")
    bus.publish(event)

    # Allow event loop to process
    await asyncio.sleep(0.01)
    assert not queue.queue.empty()
    item = await queue.queue.get()
    assert item.path == "/foo.pdf"
