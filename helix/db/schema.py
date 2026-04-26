"""
Module: helix/db/schema.py
Copyright (c) 2026 HELIX. All rights reserved.

Database schema and migrations manager using SQLAlchemy 2.0.
"""

from datetime import datetime, timezone
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncConnection
from sqlalchemy import text
from helix.config import config
import contextlib
from typing import AsyncGenerator

MIGRATIONS = [
    (1, "initial_schema", "helix/db/migrations/0001_initial.sql"),
]

async def apply_pending_migrations(conn: AsyncConnection) -> None:
    """Applies any pending migrations to the SQLite database."""
    # We must use sqlalchemy.text() for raw queries
    await conn.execute(text('''
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version         INTEGER PRIMARY KEY,
            name            TEXT NOT NULL,
            applied_at      TEXT NOT NULL
        )
    '''))

    # Get applied migrations
    result = await conn.execute(text("SELECT version FROM schema_migrations"))
    applied = {row[0] for row in result.fetchall()}

    for version, name, path in MIGRATIONS:
        if version not in applied:
            sql_content = Path(path).read_text()

            # Access the underlying aiosqlite connection correctly for async execution
            # driver_connection is the aiosqlite.Connection
            raw_conn = await conn.get_raw_connection()
            aiosqlite_conn = raw_conn.driver_connection
            await aiosqlite_conn.executescript(sql_content) # type: ignore

            await conn.execute(
                text("INSERT INTO schema_migrations VALUES (:version, :name, :applied_at)"),
                {"version": version, "name": name, "applied_at": datetime.now(timezone.utc).isoformat()}
            )

# Setup SQLAlchemy engine and session factory
db_path = Path(config.vault.index_path).expanduser() / "helix.db"
# Ensure the directory exists
db_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_async_engine(
    f"sqlite+aiosqlite:///{db_path}",
    echo=config.vault.debug,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

@contextlib.asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provides a transactional scope around a series of operations."""
    async with AsyncSessionLocal() as session:
        yield session
