import pytest
from fastapi.testclient import TestClient
import json
from pathlib import Path

from api.main import app
from core import history

client = TestClient(app)

@pytest.fixture
def temp_history_dir(tmp_path, monkeypatch):
    monkeypatch.setattr("core.history.HISTORY_DIR", tmp_path)
    
    dummy_file = tmp_path / "2026-03-22.json"
    dummy_data = [
        {"id": "1", "client_name": "toby", "question": "Test1", "record_type": "tarot", "timestamp": "2026-03-22T00:01:00", "result": {}, "interpretation": ""},
        {"id": "2", "client_name": "client_A", "question": "Test2", "record_type": "iching", "timestamp": "2026-03-22T00:02:00", "result": {}, "interpretation": ""},
        {"id": "3", "client_name": "toby", "question": "Test3", "record_type": "zhuge", "timestamp": "2026-03-22T00:03:00", "result": {}, "interpretation": ""},
        {"id": "4", "client_name": "client_B", "question": "Test4", "record_type": "daliuren", "timestamp": "2026-03-22T00:04:00", "result": {}, "interpretation": ""},
        {"id": "5", "client_name": "client_A", "question": "Test5", "record_type": "tarot", "timestamp": "2026-03-22T00:05:00", "result": {}, "interpretation": ""}
    ]
    with open(dummy_file, "w", encoding="utf-8") as f:
        json.dump(dummy_data, f)
        
    return tmp_path

def test_get_history_clients(temp_history_dir):
    response = client.get("/api/history/clients")
    assert response.status_code == 200
    clients = response.json()
    
    assert "toby" in clients
    assert "client_A" in clients
    assert "client_B" in clients
    assert len(clients) == 3

def test_get_history_with_client_filter_toby(temp_history_dir):
    response = client.get("/api/history?client_name=toby")
    assert response.status_code == 200
    records = response.json()
    
    assert len(records) == 2

def test_get_history_with_client_filter_other(temp_history_dir):
    response = client.get("/api/history?client_name=client_A")
    assert response.status_code == 200
    records = response.json()
    
    assert len(records) == 2

def test_get_history_without_filter(temp_history_dir):
    response = client.get("/api/history")
    assert response.status_code == 200
    records = response.json()
    assert len(records) == 5
