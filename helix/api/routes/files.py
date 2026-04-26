"""Files and Search REST API routes."""

from fastapi import APIRouter
from typing import Any
from pydantic import BaseModel, Field

router = APIRouter()

class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    mode: str = "hybrid"
    limit: int = Field(default=10, ge=1, le=100)

@router.get("/files")
async def list_files() -> dict[str, Any]:
    return {"success": True, "data": []}

@router.get("/files/{id}")
async def get_file(id: str) -> dict[str, Any]:
    return {"success": True, "data": {"id": id}}

@router.post("/search")
async def search(body: SearchRequest) -> dict[str, Any]:
    return {"success": True, "data": []}
