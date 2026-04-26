import pytest
from pathlib import Path
from helix.ingest.processors.pdf import PDFProcessor

def test_pdf_processor_can_handle():
    proc = PDFProcessor()
    assert proc.can_handle("application/pdf", ".pdf")
    assert proc.can_handle("unknown", ".pdf")
    assert not proc.can_handle("image/jpeg", ".jpg")

@pytest.mark.asyncio
async def test_pdf_processor_extract():
    proc = PDFProcessor()
    raw = await proc.extract(Path("/fake.pdf"))
    assert raw.mime_type == "application/pdf"
    assert "Stub" in raw.text
