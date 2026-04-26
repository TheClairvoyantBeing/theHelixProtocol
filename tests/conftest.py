# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
import pytest
from unittest.mock import AsyncMock
import json
from helix.hardware import HardwareProfile

@pytest.fixture
def mock_llm_client():
    client = AsyncMock()
    client.generate.return_value = json.dumps({
        "category": "Work/Finance",
        "tags": ["invoice", "2024", "tax"],
        "summary": "An invoice document for services rendered.",
        "confidence": 0.92,
        "language": "en",
        "key_entities": []
    })
    client.embed.return_value = [[0.1] * 768]
    client.health_check.return_value = True
    return client

@pytest.fixture
def mock_hardware_tier2():
    return HardwareProfile(
        gpu_name="NVIDIA GeForce RTX 3080",
        gpu_vendor="nvidia",
        vram_gb=10.0,
        cuda_version="12.1",
        cpu_cores=16,
        cpu_arch="x86_64",
        ram_gb=32.0,
        platform="linux",
        tier=2
    )

@pytest.fixture
def test_vault(tmp_path):
    (tmp_path / "raw").mkdir()
    (tmp_path / "wiki").mkdir()
    (tmp_path / "memory" / "episodic").mkdir(parents=True)
    (tmp_path / "memory" / "semantic").mkdir(parents=True)
    (tmp_path / "self").mkdir()
    return tmp_path
