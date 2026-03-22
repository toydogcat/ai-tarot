import pytest
import os
import yaml
from pathlib import Path
from fastapi.testclient import TestClient
from api.main import app
from omegaconf import OmegaConf

client = TestClient(app)

@pytest.fixture
def mock_admin_env(tmp_path, monkeypatch):
    # Setup mock .env
    env_file = tmp_path / ".env"
    env_file.write_text("TEST_KEY=initial_value\nGEMINI_API_KEY=old_key\n")
    
    # Setup mock config dir
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    yaml_file = config_dir / "test_config.yaml"
    yaml_file.write_text("app:\n  usage_limit: 50\nmodes:\n  tarot:\n    model_name: gemini-old\n")
    
    # Mock paths in admin.py to point to our tmp_path
    monkeypatch.setattr("api.routes.admin.ENV_PATH", env_file)
    monkeypatch.setattr("api.routes.admin.CONFIG_DIR", config_dir)
    monkeypatch.setenv("ADMIN_TOKEN", "test_secret")
    monkeypatch.setattr("api.routes.admin.ADMIN_TOKEN", "test_secret")

    return {
        "env_file": env_file,
        "yaml_file": yaml_file
    }

def test_admin_update_env_forbidden():
    response = client.post(
        "/api/admin/config/env",
        headers={"X-Admin-Token": "wrong_token"},
        json={"key": "TEST_KEY", "value": "new_value"}
    )
    assert response.status_code == 403

def test_admin_update_env_success(mock_admin_env):
    response = client.post(
        "/api/admin/config/env",
        headers={"X-Admin-Token": "test_secret"},
        json={"key": "GEMINI_API_KEY", "value": "new_key_123"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    
    # Verify .env contents
    env_content = mock_admin_env["env_file"].read_text()
    assert "GEMINI_API_KEY='new_key_123'" in env_content or "GEMINI_API_KEY=new_key_123" in env_content
    
    # Verify exact os.environ
    assert os.environ.get("GEMINI_API_KEY") == "new_key_123"

def test_admin_update_yaml_success(mock_admin_env):
    response = client.post(
        "/api/admin/config/yaml",
        headers={"X-Admin-Token": "test_secret"},
        json={
            "filename": "test_config.yaml",
            "updates": {
                "app.usage_limit": 100,
                "modes.tarot.model_name": "gemini-awesome"
            }
        }
    )
    assert response.status_code == 200
    
    # Verify YAML update via OmegaConf
    conf = OmegaConf.load(mock_admin_env["yaml_file"])
    assert conf.app.usage_limit == 100
    assert conf.modes.tarot.model_name == "gemini-awesome"
