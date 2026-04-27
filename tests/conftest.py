import pytest
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from helix.db.schema import apply_pending_migrations, engine as _engine, AsyncSessionLocal as _AsyncSessionLocal
from unittest.mock import AsyncMock

@pytest.fixture(scope="session", autouse=True)
def setup_db_sync():
    async def _setup():
        async with _engine.begin() as conn:
            await apply_pending_migrations(conn)
    asyncio.run(_setup())

@pytest.fixture
def mock_llm_client():
    client = AsyncMock()
    client.health_check.return_value = True
    return client

@pytest.fixture
def test_vault(tmp_path):
    (tmp_path / "raw").mkdir()
    (tmp_path / "wiki").mkdir()
    (tmp_path / "memory" / "episodic").mkdir(parents=True)
    (tmp_path / "memory" / "semantic").mkdir(parents=True)
    (tmp_path / "self").mkdir()
    return tmp_path
from helix.hardware import HardwareProfile

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
