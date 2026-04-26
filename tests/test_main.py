"""Test main entrypoint."""
import pytest
from helix.main import helix_os

@pytest.mark.asyncio
async def test_helix_os_init():
    assert helix_os is not None
