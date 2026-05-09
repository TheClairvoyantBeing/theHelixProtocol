"""
Module: helix/api/routes/files.py
Copyright (c) 2026 HELIX. All rights reserved.

Files and Search REST API routes using Pydantic schemas.
"""

from fastapi import APIRouter
from sqlalchemy import text

from helix.api.schemas import (
    SearchRequest, FileResponse, FileData, FileListResponse
)
from helix.db.schema import get_session
from helix.agents.chat_engine import chat_engine

router = APIRouter()

@router.get("/files", response_model=FileListResponse)
async def list_files(category: str | None = None, status: str | None = None, limit: int = 50) -> FileListResponse:
    """Lists indexed files from the vault."""
    async with get_session() as session:
        query = "SELECT id, file_name, file_path, category, summary, status FROM files"
        params: dict[str, str | int] = {}
        conditions = []

        if category:
            conditions.append("category = :category")
            params["category"] = category
        if status:
            conditions.append("status = :status")
            params["status"] = status

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY indexed_at DESC LIMIT :limit"
        params["limit"] = limit

        result = await session.execute(text(query), params)
        rows = result.fetchall()

    files = [FileData(id=row[0], file_name=row[1], file_path=row[2], category=row[3], summary=row[4], status=row[5]) for row in rows]
    return FileListResponse(success=True, data=files)


@router.get("/files/{id}", response_model=FileResponse)
async def get_file(id: str) -> FileResponse:
    """Retrieves a specific file by ID."""
    async with get_session() as session:
        result = await session.execute(
            text("SELECT id, file_name, file_path, category, summary, status FROM files WHERE id = :id"),
            {"id": id}
        )
        row = result.fetchone()

    if not row:
        return FileResponse(success=False, data=FileData(id=id), error={"message": "File not found"})

    return FileResponse(success=True, data=FileData(id=row[0], file_name=row[1], file_path=row[2], category=row[3], summary=row[4], status=row[5]))


@router.post("/search", response_model=FileListResponse)
async def search(body: SearchRequest) -> FileListResponse:
    """Executes a semantic or keyword search against the vault."""
    results = await chat_engine.search(body.query, mode=body.mode, limit=body.limit)

    # Convert search results to FileData objects
    files = []
    for res in results:
        meta = res.get("metadata", {})
        files.append(FileData(
            id=meta.get("file_id", "unknown"),
            file_name=meta.get("file_name", ""),
            summary=res.get("text", "")[:200],
        ))

    return FileListResponse(success=True, data=files)
