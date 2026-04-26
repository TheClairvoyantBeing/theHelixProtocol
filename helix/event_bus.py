"""Event Bus for inter-agent communication."""

from dataclasses import dataclass, field
from typing import Any, Callable
from datetime import datetime, timezone
import uuid

@dataclass
class BaseEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class FileQueued(BaseEvent):
    path: str = ""
    file_hash: str = ""
    mime_type: str = ""

@dataclass
class FileProcessed(BaseEvent):
    record: Any = None          # FileRecord Pydantic model
    is_new: bool = True         # False if updated

@dataclass
class WikiUpdated(BaseEvent):
    page_path: str = ""
    operation: str = ""         # "created" | "updated"

@dataclass
class TaskCreated(BaseEvent):
    task: Any = None            # Task Pydantic model

@dataclass
class ReminderDue(BaseEvent):
    reminder: Any = None        # Reminder Pydantic model

@dataclass
class VoiceInput(BaseEvent):
    text: str = ""
    confidence: float = 0.0
    duration_seconds: float = 0.0

@dataclass
class ChatTurn(BaseEvent):
    session_id: str = ""
    role: str = ""              # "user" | "assistant"
    content: str = ""
    turn_index: int = 0

@dataclass
class MemoryConsolidated(BaseEvent):
    facts_added: int = 0
    facts_updated: int = 0
    session_id: str = ""

@dataclass
class GraphUpdated(BaseEvent):
    nodes_added: int = 0
    edges_added: int = 0
    snapshot_path: str = ""

@dataclass
class IngestionProgress(BaseEvent):
    total: int = 0
    done: int = 0
    errors: int = 0
    current_file: str = ""

@dataclass
class SystemAlert(BaseEvent):
    level: str = "info"         # "info" | "warning" | "error" | "critical"
    message: str = ""
    action_required: bool = False

class EventBus:
    """Async Event Bus using custom pub/sub (PyMitt compatible API)."""
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable[..., Any]]] = {}

    def publish(self, event: BaseEvent) -> None:
        """Publishes an event to the bus."""
        event_name = type(event).__name__
        handlers = self._subscribers.get(event_name, [])
        for handler in handlers:
            handler(event)

    def subscribe(self, event_type: type[BaseEvent] | str, handler: Callable[..., Any]) -> None:
        """Subscribes a handler to an event type."""
        event_name = event_type if isinstance(event_type, str) else event_type.__name__
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(handler)

# Global singleton event bus
bus = EventBus()
