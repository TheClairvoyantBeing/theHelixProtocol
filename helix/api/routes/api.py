"""
Module: helix/api/routes/api.py
Copyright (c) 2026 HELIX. All rights reserved.

Full REST API routes mapping to the endpoints described in the API Spec.
All endpoints use Pydantic models for request and response structures.
Chat endpoint supports Server-Sent Events (SSE).
"""

import asyncio
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from typing import Dict, Any, AsyncGenerator
from helix.api.schemas import (
    ChatRequest, ChatSessionListResponse, EmptyDataResponse,
    TaskCreate, TaskResponse, TaskData, TaskListResponse,
    CalendarEventCreate, CalendarEventResponse, CalendarEventData, CalendarListResponse,
    GraphResponse, GraphData, NodeListResponse,
    MemoryProfileResponse, MemoryProfileData, FactListResponse, RuleListResponse,
    ExportStartRequest, ExportStartResponse, ExportStartData, ExportStatusResponse, ExportStatusData
)
from helix.agents.chat_engine import ChatEngine
from helix.event_bus import bus, ChatTurn

router = APIRouter()
chat_engine = ChatEngine() # Instantiate it for the route

# Chat
async def chat_stream_generator(session_id: str, content: str) -> AsyncGenerator[str, None]:
    """Generates a SSE stream for the chat response."""
    # Publish event
    bus.publish(ChatTurn(session_id=session_id, role="user", content=content))

    try:
        response_text = await chat_engine.generate_response(session_id, content)
        # Yield in chunks
        words = response_text.split(" ")
        for word in words:
            yield f"data: {word} \n\n"
            await asyncio.sleep(0.05)

        bus.publish(ChatTurn(session_id=session_id, role="assistant", content=response_text))
    except Exception as e:
        yield f"data: Error generating response: {str(e)}\n\n"

@router.post("/chat/message")
async def chat_message(body: ChatRequest) -> StreamingResponse:
    """Processes a chat message and returns a StreamingResponse (SSE)."""
    return StreamingResponse(chat_stream_generator(body.session_id, body.content), media_type="text/event-stream")

@router.get("/chat/sessions", response_model=ChatSessionListResponse)
async def chat_sessions() -> ChatSessionListResponse:
    """Retrieves all chat sessions."""
    return ChatSessionListResponse(success=True, data=[])

@router.get("/chat/sessions/{session_id}", response_model=ChatSessionListResponse)
async def chat_session_history(session_id: str) -> ChatSessionListResponse:
    """Retrieves history for a specific chat session."""
    return ChatSessionListResponse(success=True, data=[])

@router.delete("/chat/sessions/{session_id}", response_model=EmptyDataResponse)
async def chat_delete_session(session_id: str) -> EmptyDataResponse:
    """Deletes a chat session."""
    return EmptyDataResponse(success=True, data={})

@router.post("/chat/memory/wipe", response_model=EmptyDataResponse)
async def chat_memory_wipe(body: Dict[str, Any]) -> EmptyDataResponse:
    """Wipes memory for the chat engine."""
    return EmptyDataResponse(success=True, data={})

# Tasks
@router.get("/tasks", response_model=TaskListResponse)
async def list_tasks() -> TaskListResponse:
    """Retrieves list of tasks."""
    return TaskListResponse(success=True, data=[])

@router.post("/tasks", response_model=TaskResponse)
async def create_task(body: TaskCreate) -> TaskResponse:
    """Creates a new task."""
    return TaskResponse(success=True, data=TaskData(id="stub_id"))

@router.put("/tasks/{id}", response_model=EmptyDataResponse)
async def update_task(id: str, body: Dict[str, Any]) -> EmptyDataResponse:
    """Updates a task."""
    return EmptyDataResponse(success=True, data={})

@router.delete("/tasks/{id}", response_model=EmptyDataResponse)
async def delete_task(id: str) -> EmptyDataResponse:
    """Deletes a task."""
    return EmptyDataResponse(success=True, data={})

@router.post("/tasks/{id}/complete", response_model=EmptyDataResponse)
async def complete_task(id: str) -> EmptyDataResponse:
    """Marks a task as complete."""
    return EmptyDataResponse(success=True, data={})

@router.get("/tasks/overdue", response_model=TaskListResponse)
async def get_overdue_tasks() -> TaskListResponse:
    """Retrieves overdue tasks."""
    return TaskListResponse(success=True, data=[])

# Calendar
@router.get("/calendar/events", response_model=CalendarListResponse)
async def get_calendar_events(start: str | None = None, end: str | None = None) -> CalendarListResponse:
    """Retrieves calendar events."""
    return CalendarListResponse(success=True, data=[])

@router.post("/calendar/events", response_model=CalendarEventResponse)
async def create_calendar_event(body: CalendarEventCreate) -> CalendarEventResponse:
    """Creates a calendar event."""
    return CalendarEventResponse(success=True, data=CalendarEventData(id="stub_id"))

@router.put("/calendar/events/{id}", response_model=EmptyDataResponse)
async def update_calendar_event(id: str, body: Dict[str, Any]) -> EmptyDataResponse:
    """Updates a calendar event."""
    return EmptyDataResponse(success=True, data={})

@router.delete("/calendar/events/{id}", response_model=EmptyDataResponse)
async def delete_calendar_event(id: str) -> EmptyDataResponse:
    """Deletes a calendar event."""
    return EmptyDataResponse(success=True, data={})

@router.get("/calendar/export.ical")
async def export_calendar_ical() -> str:
    """Exports calendar in iCal format."""
    return "BEGIN:VCALENDAR..."

# Graph
@router.get("/graph", response_model=GraphResponse)
async def get_graph() -> GraphResponse:
    """Retrieves the knowledge graph nodes and edges."""
    return GraphResponse(success=True, data=GraphData(nodes=[], edges=[]))

@router.get("/graph/neighbours/{node_id}", response_model=NodeListResponse)
async def get_graph_neighbours(node_id: str) -> NodeListResponse:
    """Retrieves neighbours for a specific graph node."""
    return NodeListResponse(success=True, data=[])

@router.get("/graph/export.svg")
async def export_graph_svg() -> str:
    """Exports graph as SVG."""
    return "<svg></svg>"

@router.get("/graph/export.json", response_model=EmptyDataResponse)
async def export_graph_json() -> EmptyDataResponse:
    """Exports graph as JSON."""
    return EmptyDataResponse(success=True, data={})

# Memory
@router.get("/memory/profile", response_model=MemoryProfileResponse)
async def get_memory_profile() -> MemoryProfileResponse:
    """Retrieves memory profile."""
    return MemoryProfileResponse(success=True, data=MemoryProfileData(markdown=""))

@router.get("/memory/facts", response_model=FactListResponse)
async def get_memory_facts() -> FactListResponse:
    """Retrieves memory facts."""
    return FactListResponse(success=True, data=[])

@router.delete("/memory/facts/{id}", response_model=EmptyDataResponse)
async def delete_memory_fact(id: str) -> EmptyDataResponse:
    """Deletes a memory fact."""
    return EmptyDataResponse(success=True, data={})

@router.get("/memory/rules", response_model=RuleListResponse)
async def get_memory_rules() -> RuleListResponse:
    """Retrieves memory reflex rules."""
    return RuleListResponse(success=True, data=[])

@router.delete("/memory/rules/{id}", response_model=EmptyDataResponse)
async def delete_memory_rule(id: str) -> EmptyDataResponse:
    """Deletes a memory reflex rule."""
    return EmptyDataResponse(success=True, data={})

# Export
@router.post("/export/start", response_model=ExportStartResponse)
async def start_export(body: ExportStartRequest) -> ExportStartResponse:
    """Starts an export job."""
    return ExportStartResponse(success=True, data=ExportStartData(job_id="stub_job"))

@router.get("/export/status/{job_id}", response_model=ExportStatusResponse)
async def get_export_status(job_id: str) -> ExportStatusResponse:
    """Retrieves status of an export job."""
    return ExportStatusResponse(success=True, data=ExportStatusData(status="done"))

@router.get("/export/download/{job_id}", response_model=EmptyDataResponse)
async def download_export(job_id: str) -> EmptyDataResponse:
    """Downloads the completed export."""
    return EmptyDataResponse(success=True, data={})

# System Extra
@router.get("/status/hardware", response_model=EmptyDataResponse)
async def get_hardware_status() -> EmptyDataResponse:
    """Retrieves hardware status."""
    return EmptyDataResponse(success=True, data={})

@router.get("/status/models", response_model=EmptyDataResponse)
async def get_models_status() -> EmptyDataResponse:
    """Retrieves models status."""
    return EmptyDataResponse(success=True, data={})

@router.post("/admin/backup", response_model=EmptyDataResponse)
async def backup_db() -> EmptyDataResponse:
    """Backups the database manually."""
    return EmptyDataResponse(success=True, data={})

@router.post("/admin/reindex-all", response_model=EmptyDataResponse)
async def reindex_all() -> EmptyDataResponse:
    """Reindexes all files."""
    return EmptyDataResponse(success=True, data={})

@router.get("/admin/logs", response_model=EmptyDataResponse)
async def get_logs() -> EmptyDataResponse:
    """Retrieves recent logs."""
    return EmptyDataResponse(success=True, data={})

# Voice
@router.post("/voice/transcribe", response_model=EmptyDataResponse)
async def transcribe_voice() -> EmptyDataResponse:
    """Transcribes a voice clip."""
    return EmptyDataResponse(success=True, data={})
