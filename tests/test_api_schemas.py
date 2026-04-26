import pytest
from helix.api.schemas import BaseResponse

def test_base_response():
    resp = BaseResponse(success=True)
    assert resp.success is True
