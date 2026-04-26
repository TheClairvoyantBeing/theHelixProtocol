# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
import pytest
import asyncio
from pathlib import Path
from helix.ingest.watcher import FileWatcher
from helix.event_bus import bus, FileQueued

@pytest.mark.asyncio
async def test_watcher_queue_file(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello")

    watcher = FileWatcher()
    received = []
    def handler(event):
        received.append(event)
    bus.subscribe(FileQueued, handler)

    watcher.queue_file(test_file)
    assert len(received) == 1
    assert received[0].path == str(test_file)

@pytest.mark.asyncio
async def test_watcher_start_stop():
    watcher = FileWatcher()
    await watcher.start()
    assert watcher._running is True
    await watcher.stop()
    assert watcher._running is False
