import pytest
import json

from core.zhuge import interpreter as zhuge_interp
from core.daliuren import interpreter as daliuren_interp
from core.config_manager import ConfigManager

class MockGenerateContentResponse:
    def __init__(self, text):
        self.text = text

class MockModels:
    def __init__(self, response_text):
        self.response_text = response_text
        self.last_contents = None
    def generate_content(self, model, contents, config=None):
        self.last_contents = contents
        return MockGenerateContentResponse(self.response_text)

class MockClient:
    def __init__(self, response_text):
        self.models = MockModels(response_text)

@pytest.fixture
def mock_gemini(monkeypatch):
    def _create_mock(response_data):
        return MockClient(json.dumps(response_data, ensure_ascii=False))
    return _create_mock

@pytest.fixture
def temp_config_dir(tmp_path, monkeypatch):
    monkeypatch.setattr("core.config_manager.CONFIG_DIR", tmp_path)
    default_yaml = tmp_path / "default.yaml"
    default_yaml.write_text("""
guide_name: "test_toby"
prompts:
  zhuge_system: "Zhuge Sys Test"
  zhuge_requirements: "Zhuge Req Test"
  daliuren_system: "Da Liu Ren Sys Test"
  daliuren_requirements: "Da Liu Ren Req Test"
""")
    ConfigManager._instance = None
    return tmp_path

def test_interpret_zhuge_success(mock_gemini, temp_config_dir, monkeypatch):
    mock_response = {
        "reading": "成功解讀諸葛神算",
    }
    mock_client = mock_gemini(mock_response)
    monkeypatch.setattr("google.genai.Client", lambda *args, **kwargs: mock_client)
    monkeypatch.setenv("GEMINI_API_KEY", "dummy_key")
    
    result = zhuge_interp.interpret_zhuge("順利嗎", {"id": "1", "poem": "假"})
    
    assert result == "成功解讀諸葛神算"
    assert "Zhuge Sys Test" in mock_client.models.last_contents
    assert "Zhuge Req Test" in mock_client.models.last_contents

def test_interpret_daliuren_success(mock_gemini, temp_config_dir, monkeypatch):
    mock_response = {
        "reading": "大六壬測試解讀",
    }
    mock_client = mock_gemini(mock_response)
    monkeypatch.setattr("google.genai.Client", lambda *args, **kwargs: mock_client)
    monkeypatch.setenv("GEMINI_API_KEY", "dummy_key")
    
    daliuren_structure = {"pattern": "元首課", "four_classes": {}, "three_transmissions": {}}
    result = daliuren_interp.interpret_daliuren("工作如何", daliuren_structure)
    
    assert result == "大六壬測試解讀"
    assert "Da Liu Ren Sys Test" in mock_client.models.last_contents
    assert "Da Liu Ren Req Test" in mock_client.models.last_contents
