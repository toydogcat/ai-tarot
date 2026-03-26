import pytest
from fastapi.testclient import TestClient
import json
from pathlib import Path

from api.main import app
from core import history

client = TestClient(app)

@pytest.fixture
def temp_history_dir(monkeypatch):
    dummy_data = [
        {"id": "1", "client_id": "toby", "question": "Test1", "type": "tarot", "timestamp": "2026-03-22T00:01:00", "result": {}, "interpretation": ""},
        {"id": "2", "client_id": "client_A", "question": "Test2", "type": "iching", "timestamp": "2026-03-22T00:02:00", "result": {}, "interpretation": ""},
        {"id": "3", "client_id": "toby", "question": "Test3", "type": "zhuge", "timestamp": "2026-03-22T00:03:00", "result": {}, "interpretation": ""},
        {"id": "4", "client_id": "client_B", "question": "Test4", "type": "daliuren", "timestamp": "2026-03-22T00:04:00", "result": {}, "interpretation": ""},
        {"id": "5", "client_id": "client_A", "question": "Test5", "type": "tarot", "timestamp": "2026-03-22T00:05:00", "result": {}, "interpretation": ""}
    ]
    
    def mock_get_history_dates(mentor_id=None):
        return ["2026-03-22"]
        
    def mock_load_history(date_str, mentor_id=None):
        if date_str == "2026-03-22":
            return dummy_data
        return []

    monkeypatch.setattr("api.routes.history.get_history_dates", mock_get_history_dates)
    monkeypatch.setattr("api.routes.history.load_history", mock_load_history)
    
    return "mocked"

def test_get_history_clients(temp_history_dir):
    response = client.get("/api/history/clients")
    assert response.status_code == 200
    clients = response.json()
    
    assert "toby" in clients
    assert "client_A" in clients
    assert "client_B" in clients
    assert len(clients) == 3

def test_get_history_with_client_filter_toby(temp_history_dir):
    response = client.get("/api/history?client_id=toby")
    assert response.status_code == 200
    records = response.json()
    
    assert len(records) == 2

def test_get_history_with_client_filter_other(temp_history_dir):
    response = client.get("/api/history?client_id=client_A")
    assert response.status_code == 200
    records = response.json()
    
    assert len(records) == 2

def test_get_history_without_filter(temp_history_dir):
    response = client.get("/api/history")
    assert response.status_code == 200
    records = response.json()
    assert len(records) == 5
