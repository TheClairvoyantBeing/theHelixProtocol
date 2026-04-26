import pytest
import aiosqlite
from helix.db.schema import apply_pending_migrations

@pytest.mark.asyncio
async def test_apply_migrations():
    # Use in-memory SQLite for testing
    async with aiosqlite.connect(":memory:") as conn:
        await apply_pending_migrations(conn)

        # Verify schema_migrations table was created and populated
        async with conn.execute("SELECT version, name FROM schema_migrations") as cursor:
            rows = await cursor.fetchall()
            assert len(rows) == 1
            assert rows[0][0] == 1
            assert rows[0][1] == "initial_schema"

        # Verify a core table like 'files' was created
        async with conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='files'") as cursor:
            row = await cursor.fetchone()
            assert row is not None
            assert row[0] == "files"
