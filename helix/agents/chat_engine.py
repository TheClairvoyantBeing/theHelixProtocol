# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
"""ChatEngine agent handles the conversational loop and querying."""

import asyncio
import logging
from typing import Any, AsyncGenerator
from helix.event_bus import bus, ChatTurn
from helix.llm_client import llm_client
from helix.db.vector_store import vector_store

logger = logging.getLogger(__name__)

class ChatEngine:
    """Agent handling user queries and conversation."""

    def __init__(self) -> None:
        self._stop_event = asyncio.Event()
        self._tasks: list[asyncio.Task[Any]] = []
        bus.subscribe(ChatTurn, self._on_chat_turn)

    def _on_chat_turn(self, event: ChatTurn) -> None:
        logger.debug(f"ChatEngine processing ChatTurn for session {event.session_id}")
        # In a full implementation, this might asynchronously trigger memory consolidation
        # or graph queries.

    async def search(self, query: str, mode: str = "hybrid", limit: int = 10) -> list[dict[str, Any]]:
        """Semantic/hybrid search method via VectorStore."""
        logger.debug(f"ChatEngine search: query='{query}' mode='{mode}'")
        try:
            # Generate embedding for the query
            embeddings = await llm_client.embed([query])
            if not embeddings:
                return []

            # Query the chunks collection
            results = vector_store.query("helix_chunks", query_embeddings=embeddings, n_results=limit)

            # Format results
            formatted_results = []
            if results and "documents" in results and results["documents"]:
                for i, doc_list in enumerate(results["documents"]):
                    if doc_list: # chroma returns a list of lists depending on input size
                        for j, doc in enumerate(doc_list):
                            meta = results["metadatas"][i][j] if "metadatas" in results and results["metadatas"] else {}
                            dist = results["distances"][i][j] if "distances" in results and results["distances"] else 0.0
                            formatted_results.append({
                                "text": doc,
                                "metadata": meta,
                                "distance": dist
                            })
            return formatted_results
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def _build_prompt(self, content: str, search_results: list[dict[str, Any]]) -> tuple[str, str]:
        """Build system and user prompts with RAG context."""
        system_prompt = "You are HELIX, a helpful Personal Intelligence OS. Answer concisely based on the user's data vault."
        user_prompt = f"User Query: {content}\n\n"

        if search_results:
            context_str = ""
            for i, res in enumerate(search_results):
                context_str += f"Context {i+1}:\n{res['text']}\n\n"
            user_prompt += f"Relevant Vault Information:\n{context_str}"

        return system_prompt, user_prompt

    async def generate_response(self, session_id: str, content: str) -> str:
        """Generates a response using the LLMClient (non-streaming)."""
        logger.info(f"Generating response for {session_id}")

        search_results = await self.search(content, limit=3)
        system_prompt, user_prompt = self._build_prompt(content, search_results)

        try:
            response = await llm_client.generate(prompt=user_prompt, system=system_prompt)
            return response
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return f"I encountered an error trying to process your request: {e}"

    async def generate_response_stream(self, session_id: str, content: str) -> AsyncGenerator[str, None]:
        """Generates a streaming response using the LLM streaming API for real SSE."""
        logger.info(f"Generating streaming response for {session_id}")

        search_results = await self.search(content, limit=3)
        system_prompt, user_prompt = self._build_prompt(content, search_results)

        try:
            async for chunk in llm_client.generate_stream(prompt=user_prompt, system=system_prompt):
                yield chunk
        except Exception as e:
            logger.error(f"Streaming response generation failed: {e}")
            yield f"I encountered an error trying to process your request: {e}"

    async def run(self) -> None:
        while not self._stop_event.is_set():
            await asyncio.sleep(1.0)

    async def stop(self) -> None:
        self._stop_event.set()
        if self._tasks:
            await asyncio.wait(self._tasks, timeout=30.0)
        logger.info("ChatEngine stopped.")

# Shared instance export to avoid duplication across routes/main
chat_engine = ChatEngine()
