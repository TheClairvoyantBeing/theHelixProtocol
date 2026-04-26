# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
import pytest
import asyncio
from helix.voice.voice_gate import VoiceGate
from helix.config import config

@pytest.mark.asyncio
async def test_voice_gate_disabled():
    config.voice.enabled = False
    gate = VoiceGate()
    await gate.start()
    assert gate._running is False

@pytest.mark.asyncio
async def test_voice_gate_stop():
    config.voice.enabled = True
    gate = VoiceGate()
    await gate.start()
    assert gate._running is True
    await gate.stop()
    assert gate._running is False
