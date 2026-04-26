import pytest
from helix.ingest.router import FileRouter
from helix.ingest.processors.image import ImageProcessor
from helix.ingest.processors.pdf import PDFProcessor

def test_router_get_processor():
    router = FileRouter()

    # Test Exact Match
    proc = router.get_processor("image/jpeg", ".jpg")
    assert proc is ImageProcessor

    # Test Fallback match
    proc = router.get_processor("application/pdf", ".pdf")
    assert proc is PDFProcessor

    proc = router.get_processor("unknown/type", ".bin")
    assert proc is None
