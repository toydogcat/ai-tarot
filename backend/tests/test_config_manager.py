import pytest
from pathlib import Path
from core.config_manager import ConfigManager, CONFIG_DIR

@pytest.fixture
def temp_config_dir(tmp_path, monkeypatch):
    monkeypatch.setattr("core.config_manager.CONFIG_DIR", tmp_path)
    default_yaml = tmp_path / "default.yaml"
    default_yaml.write_text("""
guide_name: "test_toby"
prompts:
  tarot_system: "Test tarot system"
""")
    # Reset singleton instance
    ConfigManager._instance = None
    return tmp_path

def test_config_manager_get_default(temp_config_dir):
    manager = ConfigManager()
    assert manager.active_profile in ["default", "customer1", "customer2", "tmp"]
    
def test_config_manager_save(temp_config_dir):
    manager = ConfigManager()
    manager.set_active_profile("customer1")
    manager.config.guide_name = "saved_toby"
    manager.save()
    
    saved_content = (temp_config_dir / "customer1.yaml").read_text(encoding="utf-8")
    assert "guide_name: saved_toby" in saved_content
