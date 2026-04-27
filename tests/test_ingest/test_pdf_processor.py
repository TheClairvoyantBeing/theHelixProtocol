import pytest
from pathlib import Path
from helix.ingest.processors.pdf import PDFProcessor

def test_pdf_processor_can_handle():
    proc = PDFProcessor()
    assert proc.can_handle("application/pdf", ".pdf")
    assert not proc.can_handle("image/jpeg", ".jpg")

@pytest.mark.asyncio
async def test_pdf_processor_extract():
    proc = PDFProcessor()
    # It attempts to open the file. Instead of creating a real PDF in the test,
    # we can just test that it handles errors gracefully if we don't mock it,
    # or test the type.
    raw = await proc.extract(Path("/fake.pdf"))
    assert raw.mime_type == "application/pdf"
    assert "Error extracting PDF" in raw.text
