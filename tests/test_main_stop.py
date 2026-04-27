"""
Module: tests/test_main_stop.py
Copyright (c) 2026 HELIX. All rights reserved.

Test main stop.
"""
import pytest
import asyncio
from helix.main import helix_os

@pytest.mark.asyncio
async def test_helix_os_shutdown():
    await helix_os.stop()
