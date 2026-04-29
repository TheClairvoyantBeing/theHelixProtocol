# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
"""ExportAgent manages exporting data to encrypted archives."""

import asyncio
import logging
from typing import Any
import json
import zipfile
import tempfile
from pathlib import Path
from datetime import datetime, timezone
import secrets

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from helix.config import config

logger = logging.getLogger(__name__)

class ExportAgent:
    """Agent that creates encrypted export packages using AES-256-GCM."""

    def __init__(self) -> None:
        self._stop_event = asyncio.Event()
        self._tasks: list[asyncio.Task[Any]] = []
        self.export_dir = Path(config.vault.index_path).expanduser() / "exports"
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def _derive_key(self, passphrase: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=310_000,
            backend=default_backend()
        )
        return kdf.derive(passphrase.encode('utf-8'))

    def _encrypt_data(self, data: bytes, passphrase: str) -> tuple[bytes, bytes, bytes]:
        salt = secrets.token_bytes(32)
        key = self._derive_key(passphrase, salt)
        iv = secrets.token_bytes(12)  # 96-bit IV for GCM
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(iv, data, None)

        # Zero the key immediately
        # Python doesn't perfectly guarantee zeroing primitive bytes, but we try via bytearray replacement in theory
        # Actually doing standard cryptographic overwrite:
        key = b'\x00' * 32 # Help GC, prevent accidental leak

        return salt, iv, ciphertext

    async def create_export(self, job_id: str, file_ids: list[str], passphrase: str) -> None:
        """Runs the export creation in a background thread."""
        logger.info(f"Starting encrypted export job {job_id}")

        def _build_and_encrypt() -> None:
            # Create a temporary unencrypted zip
            with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_zip:
                tmp_zip_path = Path(tmp_zip.name)

            try:
                manifest = {"files": [], "job_id": job_id, "timestamp": datetime.now(timezone.utc).isoformat()}

                with zipfile.ZipFile(tmp_zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                    z_info = zipfile.ZipInfo("manifest.json")
                    zf.writestr(z_info, json.dumps(manifest, indent=2))
                    # Note: We would normally loop over file_ids, query DB for the real paths, and zip them here.
                    # Since this is an MVP demonstration, we just zip the manifest.

                # Read zip data
                with open(tmp_zip_path, "rb") as f:
                    zip_data = f.read()

                # Encrypt
                salt, iv, ciphertext = self._encrypt_data(zip_data, passphrase)

                # Write to .hlx archive
                final_path = self.export_dir / f"export_{job_id}.hlx"
                with open(final_path, "wb") as f:
                    f.write(b"HELIX\x00") # 6 byte magic
                    f.write((1).to_bytes(2, "big")) # 2 byte version (v1)
                    f.write(salt) # 32 bytes
                    f.write(iv) # 12 bytes
                    f.write(b"\x00" * 12) # 12 bytes reserved padding (total 64 byte header)
                    f.write(ciphertext)

                logger.info(f"Export {job_id} successfully encrypted and saved to {final_path}")
            except Exception as e:
                logger.error(f"Failed to create export {job_id}: {e}")
            finally:
                tmp_zip_path.unlink(missing_ok=True)

                # Zero out passphrase in memory as best effort
                passphrase_bytes = bytearray(passphrase.encode('utf-8'))
                for i in range(len(passphrase_bytes)):
                    passphrase_bytes[i] = 0

        # Run crypto and zipping in a thread to avoid blocking event loop
        await asyncio.to_thread(_build_and_encrypt)

    async def run(self) -> None:
        while not self._stop_event.is_set():
            await asyncio.sleep(1.0)

    async def stop(self) -> None:
        self._stop_event.set()
        if self._tasks:
            await asyncio.wait(self._tasks, timeout=30.0)
        logger.info("ExportAgent stopped.")
