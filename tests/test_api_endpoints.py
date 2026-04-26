import pytest
from fastapi.testclient import TestClient
from helix.api.app import app

client = TestClient(app)

def test_status_endpoint():
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_files_endpoint():
    response = client.get("/api/v1/files")
    assert response.status_code == 200

def test_tasks_endpoint():
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
