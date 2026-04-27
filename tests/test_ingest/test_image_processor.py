import pytest
from pathlib import Path
from helix.ingest.processors.image import ImageProcessor

def test_image_processor_can_handle():
    proc = ImageProcessor()
    assert proc.can_handle("image/jpeg", ".jpg")
    assert proc.can_handle("image/png", ".png")
    assert not proc.can_handle("application/pdf", ".pdf")

@pytest.mark.asyncio
async def test_image_processor_extract(tmp_path):
    proc = ImageProcessor()

    from PIL import Image
    test_img = tmp_path / "test.jpg"
    img = Image.new('RGB', (100, 100), color = 'red')
    img.save(test_img)

    raw = await proc.extract(test_img)
    assert raw.mime_type == "image/jpeg"
    assert raw.metadata["format"] == "JPEG"
