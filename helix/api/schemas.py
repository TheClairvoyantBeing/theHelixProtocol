"""
Module: helix/api/schemas.py
Copyright (c) 2026 HELIX. All rights reserved.

Pydantic schemas for all API requests and responses.
Using Pydantic v2 to strictly avoid passing raw dicts between layers.
"""

from pydantic import BaseModel, Field, constr
from typing import Literal

# --- Common Responses ---
class BaseResponse(BaseModel):
    """Base API Response wrapper."""
    success: bool
    error: dict[str, str] | None = None

class EmptyDataResponse(BaseResponse):
    """Response containing no specific data."""
    data: dict[str, str] | None = None

# --- Files API ---
class SearchRequest(BaseModel):
    """Request schema for semantic search."""
    query: constr(min_length=1, max_length=2000) # type: ignore
    mode: Literal['semantic', 'keyword', 'hybrid'] = 'hybrid'
    limit: int = Field(default=10, ge=1, le=100)

class FileData(BaseModel):
    """Data schema representing a file."""
    id: str

class FileResponse(BaseResponse):
    """Response containing a single file."""
    data: FileData

class FileListResponse(BaseResponse):
    """Response containing a list of files."""
    data: list[FileData]

class StatusData(BaseModel):
    """System health status."""
    status: str

class StatusResponse(BaseResponse):
    """Response containing system status."""
    data: StatusData

# --- Chat API ---
class ChatRequest(BaseModel):
    """Request schema for a chat message."""
    session_id: str
    content: str

class ChatData(BaseModel):
    """Data schema for chat response."""
    response: str

class ChatResponse(BaseResponse):
    """Response containing chat output."""
    data: ChatData

class ChatSessionListResponse(BaseResponse):
    """Response containing chat sessions."""
    data: list[str]

# --- Tasks API ---
class TaskCreate(BaseModel):
    """Request schema for creating a task."""
    title: str
    deadline: str | None = None
    priority: str = "medium"

class TaskData(BaseModel):
    """Data schema representing a task ID."""
    id: str

class TaskResponse(BaseResponse):
    """Response containing a single task ID."""
    data: TaskData

class TaskListResponse(BaseResponse):
    """Response containing a list of tasks."""
    data: list[str]

# --- Calendar API ---
class CalendarEventCreate(BaseModel):
    """Request schema to create a calendar event."""
    title: str

class CalendarEventData(BaseModel):
    """Data schema for a calendar event."""
    id: str

class CalendarEventResponse(BaseResponse):
    """Response containing a calendar event ID."""
    data: CalendarEventData

class CalendarListResponse(BaseResponse):
    """Response containing a list of events."""
    data: list[str]

# --- Graph API ---
class GraphData(BaseModel):
    """Data schema representing graph nodes and edges."""
    nodes: list[str]
    edges: list[str]

class GraphResponse(BaseResponse):
    """Response containing full graph."""
    data: GraphData

class NodeListResponse(BaseResponse):
    """Response containing list of nodes."""
    data: list[str]

# --- Memory API ---
class MemoryProfileData(BaseModel):
    """Data schema for memory profile."""
    markdown: str

class MemoryProfileResponse(BaseResponse):
    """Response containing memory profile."""
    data: MemoryProfileData

class FactListResponse(BaseResponse):
    """Response containing list of facts."""
    data: list[str]

class RuleListResponse(BaseResponse):
    """Response containing list of rules."""
    data: list[str]

# --- Export API ---
class ExportStartRequest(BaseModel):
    """Request to start an export job."""
    mode: str

class ExportStartData(BaseModel):
    """Data schema containing export job ID."""
    job_id: str

class ExportStartResponse(BaseResponse):
    """Response containing export job ID."""
    data: ExportStartData

class ExportStatusData(BaseModel):
    """Data schema for export status."""
    status: str

class ExportStatusResponse(BaseResponse):
    """Response containing export status."""
    data: ExportStatusData
