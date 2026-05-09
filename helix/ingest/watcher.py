"""
Module: helix/ingest/watcher.py
Copyright (c) 2026 HELIX. All rights reserved.

File watcher module to emit FileQueued events.
Scans configured vault directories and queues new/changed files for ingestion.
"""

import asyncio
import hashlib
import mimetypes
from pathlib import Path
from typing import Any
from helix.event_bus import bus, FileQueued
from helix.config import config
from helix.db.schema import get_session
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)

# Try to import python-magic for accurate MIME detection, fall back to stdlib
try:
    import magic
    _HAS_MAGIC = True
except ImportError:
    _HAS_MAGIC = False
    logger.warning("python-magic not available, falling back to mimetypes.guess_type()")


def _detect_mime(file_path: Path) -> str:
    """Detect MIME type using python-magic if available, else stdlib mimetypes."""
    if _HAS_MAGIC:
        try:
            return magic.from_file(str(file_path), mime=True)
        except Exception:
            pass
    mime, _ = mimetypes.guess_type(str(file_path))
    return mime or "application/octet-stream"


def _hash_file(file_path: Path) -> str:
    """Compute SHA-256 hash for file deduplication."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


# File extensions to skip during scanning
_SKIP_EXTENSIONS = {
    ".ds_store", ".thumbs.db", ".gitignore", ".git",
    ".pyc", ".pyo", ".swp", ".swo", ".tmp", ".lock",
}

# Max file size to ingest (from config, default 500MB)
_MAX_FILE_SIZE_BYTES = config.processing.max_file_size_mb * 1024 * 1024


class FileWatcher:
    """Watches the vault for new files to index."""

    def __init__(self) -> None:
        self._running = False
        self._task: asyncio.Task[Any] | None = None
        self._known_hashes: dict[str, str] = {}  # path -> hash cache

    async def start(self) -> None:
        self._running = True
        # Pre-load known file hashes from DB to avoid re-processing
        await self._load_known_hashes()
        self._task = asyncio.create_task(self._watch_loop())
        logger.info("FileWatcher started.")

    async def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("FileWatcher stopped.")

    async def _load_known_hashes(self) -> None:
        """Load existing file hashes from database to avoid reprocessing."""
        try:
            async with get_session() as session:
                result = await session.execute(
                    text("SELECT file_path, file_hash FROM files WHERE status = 'done'")
                )
                for row in result.fetchall():
                    self._known_hashes[row[0]] = row[1]
            logger.info(f"FileWatcher loaded {len(self._known_hashes)} known file hashes.")
        except Exception as e:
            logger.error(f"Failed to load known hashes: {e}")

    async def _watch_loop(self) -> None:
        """
        Polls configured vault directories for new/changed files.
        Runs an initial full scan, then polls every 30 seconds.
        """
        # Initial scan on startup
        await self._scan_all_vaults()

        while self._running:
            await asyncio.sleep(30.0)
            if self._running:
                await self._scan_all_vaults()

    async def _scan_all_vaults(self) -> None:
        """Scans all configured vault root directories for new or changed files."""
        queued_count = 0
        for root_dir_str in config.vault.root_dirs:
            root_path = Path(root_dir_str).expanduser()
            if not root_path.exists() or not root_path.is_dir():
                logger.debug(f"Vault directory does not exist, skipping: {root_path}")
                continue

            try:
                for file_path in root_path.rglob("*"):
                    if not self._running:
                        return

                    if not file_path.is_file():
                        continue

                    # Skip hidden files and known junk
                    if file_path.name.startswith("."):
                        continue
                    if file_path.suffix.lower() in _SKIP_EXTENSIONS:
                        continue

                    # Skip files that are too large
                    try:
                        file_size = file_path.stat().st_size
                        if file_size > _MAX_FILE_SIZE_BYTES or file_size == 0:
                            continue
                    except OSError:
                        continue

                    # Check if file has changed since last scan
                    path_str = str(file_path)
                    try:
                        file_hash = _hash_file(file_path)
                    except (OSError, PermissionError) as e:
                        logger.debug(f"Cannot read {file_path}: {e}")
                        continue

                    known_hash = self._known_hashes.get(path_str)
                    if known_hash == file_hash:
                        continue  # File unchanged, skip

                    # New or changed file — queue it
                    mime_type = _detect_mime(file_path)
                    event = FileQueued(path=path_str, file_hash=file_hash, mime_type=mime_type)
                    bus.publish(event)

                    # Update local cache
                    self._known_hashes[path_str] = file_hash
                    queued_count += 1

            except Exception as e:
                logger.error(f"Error scanning vault directory {root_path}: {e}")

        if queued_count > 0:
            logger.info(f"FileWatcher queued {queued_count} new/changed files for ingestion.")

    def queue_file(self, file_path: Path) -> None:
        """Manually queues a single file for ingestion."""
        if not file_path.exists() or not file_path.is_file():
            return

        try:
            mime_type = _detect_mime(file_path)
            file_hash = _hash_file(file_path)

            event = FileQueued(path=str(file_path), file_hash=file_hash, mime_type=mime_type)
            bus.publish(event)
            self._known_hashes[str(file_path)] = file_hash
            logger.info(f"Manually queued: {file_path.name}")
        except Exception as e:
            logger.error(f"Error queueing file {file_path}: {e}")
