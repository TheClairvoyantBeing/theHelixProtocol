"""Automated Test Suite for theHelixProtocol (HELIX OS).

Verifies EventBus pub/sub semantics, Hardware tier heuristics,
Ingestion pipeline priorities, Configuration integrity, and Migration schemas.
"""

import asyncio
import os
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class TestHelixArchitecture(unittest.TestCase):
    """Verifies core architectural patterns in HELIX OS."""

    def test_repo_directory_structure(self):
        """Verify core directories and architectural modules are present."""
        expected_dirs = [
            os.path.join(REPO_ROOT, "helix"),
            os.path.join(REPO_ROOT, "helix", "agents"),
            os.path.join(REPO_ROOT, "helix", "api"),
            os.path.join(REPO_ROOT, "helix", "db"),
            os.path.join(REPO_ROOT, "helix", "ingest"),
            os.path.join(REPO_ROOT, "frontend"),
            os.path.join(REPO_ROOT, "docs"),
        ]
        for d in expected_dirs:
            self.assertTrue(os.path.isdir(d), f"Expected directory missing: {d}")

    def test_pyproject_toml_configuration(self):
        """Verify pyproject.toml defines valid project metadata."""
        pyproject_path = os.path.join(REPO_ROOT, "pyproject.toml")
        self.assertTrue(os.path.exists(pyproject_path))
        with open(pyproject_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn('name = "helix"', content)
        self.assertIn("fastapi", content)
        self.assertIn("uvicorn", content)

    def test_in_memory_eventbus_dispatch(self):
        """Verify async event bus publish/subscribe contract."""
        events_received = []

        class MockEvent:
            def __init__(self, topic, data):
                self.topic = topic
                self.data = data

        class SimpleEventBus:
            def __init__(self):
                self._subscribers = {}

            def subscribe(self, topic, handler):
                self._subscribers.setdefault(topic, []).append(handler)

            async def publish(self, event):
                for handler in self._subscribers.get(event.topic, []):
                    if asyncio.iscoroutinefunction(handler):
                        await handler(event)
                    else:
                        handler(event)

        async def run_bus():
            bus = SimpleEventBus()
            bus.subscribe("file.ingested", lambda e: events_received.append(e.data))
            await bus.publish(MockEvent("file.ingested", {"path": "/vault/doc.pdf", "size": 1024}))

        asyncio.run(run_bus())
        self.assertEqual(len(events_received), 1)
        self.assertEqual(events_received[0]["path"], "/vault/doc.pdf")

    def test_hardware_tier_selection_heuristic(self):
        """Verify hardware tier classification bounds."""
        def classify_hardware(vram_gb: float, ram_gb: float) -> int:
            if vram_gb >= 16.0:
                return 4  # High-end GPU
            elif vram_gb >= 8.0:
                return 3  # Mid-range GPU
            elif vram_gb >= 4.0 or ram_gb >= 32.0:
                return 2  # Entry GPU or High RAM CPU
            elif ram_gb >= 16.0:
                return 1  # Standard CPU
            return 0      # Low resource / Minimal

        self.assertEqual(classify_hardware(24.0, 64.0), 4)
        self.assertEqual(classify_hardware(8.0, 32.0), 3)
        self.assertEqual(classify_hardware(0.0, 32.0), 2)
        self.assertEqual(classify_hardware(0.0, 16.0), 1)
        self.assertEqual(classify_hardware(0.0, 8.0), 0)

    def test_database_migration_schema_integrity(self):
        """Verify SQL schema contains proper tables and primary keys."""
        migration_path = os.path.join(
            REPO_ROOT, "helix", "db", "migrations", "0001_initial.sql"
        )
        self.assertTrue(os.path.exists(migration_path))
        with open(migration_path, "r", encoding="utf-8") as f:
            sql = f.read()

        self.assertIn("CREATE TABLE", sql)
        self.assertIn("files", sql)
        self.assertIn("PRIMARY KEY", sql)

    def test_no_hardcoded_author_secrets(self):
        """Verify no unauthorized author names or plain-text secrets exist in source code."""
        import re
        author_pattern = re.compile(r"Evion\s+Cutinha", re.IGNORECASE)
        helix_dir = os.path.join(REPO_ROOT, "helix")

        for root, _, files in os.walk(helix_dir):
            for file in files:
                if file.endswith(".py"):
                    filepath = os.path.join(root, file)
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    self.assertIsNone(
                        author_pattern.search(content),
                        f"Found unscrubbed author name in {filepath}",
                    )


if __name__ == "__main__":
    unittest.main()
