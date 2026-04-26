import pytest
from fastapi.testclient import TestClient
from helix.api.app import app

client = TestClient(app)

def test_graph_endpoint():
    response = client.get("/api/v1/graph")
    assert response.status_code == 200

def test_memory_profile():
    response = client.get("/api/v1/memory/profile")
    assert response.status_code == 200

def test_export_start():
    response = client.post("/api/v1/export/start", json={"mode": "json"})
    assert response.status_code == 200

def test_voice_transcribe():
    response = client.post("/api/v1/voice/transcribe")
    assert response.status_code == 200
