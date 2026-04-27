# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
"""ChromaDB vector store wrapper for HELIX."""

import logging
from typing import Any, Mapping
from pathlib import Path
import chromadb
from helix.config import config

logger = logging.getLogger(__name__)

class VectorStore:
    """Wrapper around ChromaDB for storing and querying embeddings."""
    def __init__(self) -> None:
        self.db_path = Path(config.vault.index_path).expanduser() / "chroma"
        self.db_path.mkdir(parents=True, exist_ok=True)

        try:
            self.client = chromadb.PersistentClient(path=str(self.db_path))
            self.chunks_collection = self.client.get_or_create_collection("helix_chunks")
            self.memory_collection = self.client.get_or_create_collection("helix_memory")
            logger.info("ChromaDB initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            self.client = None # type: ignore
            self.chunks_collection = None # type: ignore
            self.memory_collection = None # type: ignore

    def add_embeddings(self, collection_name: str, embeddings: list[Any], documents: list[str], metadatas: list[Mapping[str, Any]], ids: list[str]) -> None:
        """Adds embeddings to the specified collection."""
        if not self.client:
            logger.error("ChromaDB is not initialized.")
            return

        try:
            collection = self.chunks_collection if collection_name == "helix_chunks" else self.memory_collection
            if collection:
                collection.add(
                    embeddings=embeddings,
                    documents=documents,
                    metadatas=metadatas, # type: ignore
                    ids=ids
                )
                logger.debug(f"Added {len(embeddings)} embeddings to {collection_name}")
        except Exception as e:
            logger.error(f"Failed to add embeddings: {e}")

    def query(self, collection_name: str, query_embeddings: list[Any], n_results: int = 10, where: dict[str, Any] | None = None) -> dict[str, Any]:
        """Queries the specified collection."""
        if not self.client:
            logger.error("ChromaDB is not initialized.")
            return {"documents": [], "metadatas": [], "distances": []}

        try:
            collection = self.chunks_collection if collection_name == "helix_chunks" else self.memory_collection
            if collection:
                results = collection.query(
                    query_embeddings=query_embeddings,
                    n_results=n_results,
                    where=where,
                    include=["documents", "metadatas", "distances"]
                )
                return results # type: ignore
        except Exception as e:
            logger.error(f"Query to {collection_name} failed: {e}")

        return {"documents": [], "metadatas": [], "distances": []}

# Global singleton
vector_store = VectorStore()
