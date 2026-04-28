# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
"""GraphBuilder agent constructs the knowledge graph from files and wiki pages."""

import asyncio
import logging
from typing import Any
from pathlib import Path
import json
from datetime import datetime, timezone
from sqlalchemy import text

from helix.event_bus import bus, FileProcessed, WikiUpdated, GraphUpdated
from helix.db.schema import get_session

logger = logging.getLogger(__name__)

class GraphBuilder:
    """Agent that builds a property graph in SQLite for nodes and edges."""

    def __init__(self) -> None:
        self._stop_event = asyncio.Event()
        self._tasks: list[asyncio.Task[Any]] = []

        bus.subscribe(FileProcessed, self._on_file_processed)
        bus.subscribe(WikiUpdated, self._on_wiki_updated)

    async def _on_file_processed(self, event: FileProcessed) -> None:
        try:
            file_record = event.record
            if not isinstance(file_record, dict) or "id" not in file_record:
                return

            file_id = file_record["id"]

            async with get_session() as session:
                result = await session.execute(
                    text("SELECT file_name, category, tags FROM files WHERE id = :id"),
                    {"id": file_id}
                )
                row = result.fetchone()
                if not row:
                    return

                file_name, category, tags_json = row
                now_str = datetime.now(timezone.utc).isoformat()

                # 1. Upsert File Node
                file_node_id = f"node_file_{file_id}"
                await session.execute(
                    text("""
                        INSERT INTO graph_nodes (id, label, node_type, file_id, created_at)
                        VALUES (:id, :label, 'file', :file_id, :now)
                        ON CONFLICT(id) DO UPDATE SET label = excluded.label
                    """),
                    {"id": file_node_id, "label": file_name, "file_id": file_id, "now": now_str}
                )

                nodes_added = 1
                edges_added = 0

                # 2. Extract and link Tags as Concept Nodes
                if tags_json:
                    try:
                        tags = json.loads(tags_json)
                        if isinstance(tags, list):
                            for tag in tags:
                                if not tag:
                                    continue
                                tag = tag.lower().strip()
                                tag_node_id = f"node_concept_{tag}"

                                # Upsert concept node
                                await session.execute(
                                    text("""
                                        INSERT INTO graph_nodes (id, label, node_type, created_at)
                                        VALUES (:id, :label, 'concept', :now)
                                        ON CONFLICT(id) DO NOTHING
                                    """),
                                    {"id": tag_node_id, "label": tag, "now": now_str}
                                )
                                nodes_added += 1

                                # Create edge File -> Concept
                                edge_id = f"edge_{file_node_id}_{tag_node_id}"
                                await session.execute(
                                    text("""
                                        INSERT INTO graph_edges (id, source_id, target_id, relation, weight, created_at)
                                        VALUES (:id, :src, :tgt, 'shares_tag', 1.0, :now)
                                        ON CONFLICT(source_id, target_id, relation) DO NOTHING
                                    """),
                                    {"id": edge_id, "src": file_node_id, "tgt": tag_node_id, "now": now_str}
                                )
                                edges_added += 1
                    except json.JSONDecodeError:
                        pass

                await session.commit()

            bus.publish(GraphUpdated(nodes_added=nodes_added, edges_added=edges_added))
            logger.info(f"GraphBuilder updated nodes for file: {file_name}")

        except Exception as e:
            logger.error(f"GraphBuilder failed on FileProcessed: {e}")

    async def _on_wiki_updated(self, event: WikiUpdated) -> None:
        try:
            page_path = event.page_path
            page_name = Path(page_path).stem
            now_str = datetime.now(timezone.utc).isoformat()

            async with get_session() as session:
                node_id = f"node_wiki_{page_name.lower().replace(' ', '_')}"
                await session.execute(
                    text("""
                        INSERT INTO graph_nodes (id, label, node_type, created_at)
                        VALUES (:id, :label, 'wiki_page', :now)
                        ON CONFLICT(id) DO NOTHING
                    """),
                    {"id": node_id, "label": page_name, "now": now_str}
                )
                await session.commit()

            bus.publish(GraphUpdated(nodes_added=1, edges_added=0))
        except Exception as e:
            logger.error(f"GraphBuilder failed on WikiUpdated: {e}")

    async def run(self) -> None:
        while not self._stop_event.is_set():
            await asyncio.sleep(1.0)

    async def stop(self) -> None:
        self._stop_event.set()
        if self._tasks:
            await asyncio.wait(self._tasks, timeout=30.0)
        logger.info("GraphBuilder stopped.")
