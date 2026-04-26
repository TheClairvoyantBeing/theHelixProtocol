"""
Module: tests/test_db_schema_more.py
Copyright (c) 2026 HELIX. All rights reserved.

Additional schema tests.
"""
import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from helix.db.schema import apply_pending_migrations

@pytest.mark.asyncio
async def test_apply_migrations_sqlalchemy():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await apply_pending_migrations(conn)
