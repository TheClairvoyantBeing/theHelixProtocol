import pytest
from pathlib import Path
from helix.ingest.processors.image import ImageProcessor

def test_image_processor_can_handle():
    proc = ImageProcessor()
    assert proc.can_handle("image/jpeg", ".jpg")
    assert not proc.can_handle("video/mp4", ".mp4")

@pytest.mark.asyncio
async def test_image_processor_extract():
    proc = ImageProcessor()
    raw = await proc.extract(Path("/fake.jpg"))
    assert raw.mime_type == "image/jpeg"
    assert raw.text == "Stub image text"
