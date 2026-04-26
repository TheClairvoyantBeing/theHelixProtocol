import pytest
from fastapi.testclient import TestClient
from helix.api.app import app

client = TestClient(app)

def test_chat_message():
    response = client.post("/api/v1/chat/message", json={"session_id": "1", "content": "hi"})
    assert response.status_code == 200

def test_create_task():
    response = client.post("/api/v1/tasks", json={"title": "task"})
    assert response.status_code == 200

def test_calendar_events():
    response = client.get("/api/v1/calendar/events")
    assert response.status_code == 200
