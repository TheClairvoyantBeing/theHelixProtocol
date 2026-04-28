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

MIGRATIONS_DIR = Path(__file__).parent / "migrations"

MIGRATIONS = [
    (1, "initial_schema", MIGRATIONS_DIR / "0001_initial.sql"),
]

async def apply_pending_migrations(conn: AsyncConnection) -> None:
    """Applies any pending migrations to the SQLite database."""
    await conn.execute(text('''
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version         INTEGER PRIMARY KEY,
            name            TEXT NOT NULL,
            applied_at      TEXT NOT NULL
        )
    '''))

    result = await conn.execute(text("SELECT version FROM schema_migrations"))
    applied = {row[0] for row in result.fetchall()}

    for version, name, path in MIGRATIONS:
        if version not in applied:
            if not path.exists():
                raise FileNotFoundError(f"Migration file not found: {path}")
            sql_content = path.read_text()

            raw_conn = await conn.get_raw_connection()
            aiosqlite_conn = raw_conn.driver_connection
            await aiosqlite_conn.executescript(sql_content) # type: ignore

            await conn.execute(
                text("INSERT INTO schema_migrations VALUES (:version, :name, :applied_at)"),
                {"version": version, "name": name, "applied_at": datetime.now(timezone.utc).isoformat()}
            )

db_path = Path(config.vault.index_path).expanduser() / "helix.db"
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
