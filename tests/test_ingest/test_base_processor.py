# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
import pytest
from pathlib import Path
from helix.ingest.processors.base import BaseProcessor, RawContent

class DummyProcessor(BaseProcessor, mime_patterns=["dummy/*"]):
    def can_handle(self, mime_type, ext):
        return mime_type == "dummy/test"

    async def extract(self, path):
        return RawContent(text="t", full_text="ft", frames=[], audio_path=None, metadata={}, mime_type="dummy/test", file_path=path)

def test_base_processor_registry():
    assert "dummy/*" in BaseProcessor._registry
    assert BaseProcessor._registry["dummy/*"] == DummyProcessor

@pytest.mark.asyncio
async def test_base_processor_stubs():
    proc = DummyProcessor()
    assert proc.can_handle("dummy/test", ".d")
    raw = await proc.extract(Path("/f"))
    assert raw.text == "t"

    record = await proc.generate_record(raw, None, None)
    assert record["category"] == "Unknown"
