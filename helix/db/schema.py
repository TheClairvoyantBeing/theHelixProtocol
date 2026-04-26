"""Database schema and migrations manager."""

from datetime import datetime, timezone
from pathlib import Path
import aiosqlite
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from helix.config import config

MIGRATIONS = [
    (1, "initial_schema", "helix/db/migrations/0001_initial.sql"),
]

async def apply_pending_migrations(conn: aiosqlite.Connection) -> None:
    """Applies any pending migrations to the SQLite database."""
    # Ensure migrations table exists
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version         INTEGER PRIMARY KEY,
            name            TEXT NOT NULL,
            applied_at      TEXT NOT NULL
        )
    ''')
    await conn.commit()

    # Get applied migrations
    async with conn.execute("SELECT version FROM schema_migrations") as cursor:
        rows = await cursor.fetchall()
        applied = {row[0] for row in rows}

    for version, name, path in MIGRATIONS:
        if version not in applied:
            sql = Path(path).read_text()
            await conn.executescript(sql)
            await conn.execute(
                "INSERT INTO schema_migrations VALUES (?, ?, ?)",
                (version, name, datetime.now(timezone.utc).isoformat())
            )
    await conn.commit()

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

async def get_session() -> AsyncSession: # type: ignore
    """Provides a transactional scope around a series of operations."""
    async with AsyncSessionLocal() as session:
        yield session
