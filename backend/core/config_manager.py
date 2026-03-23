import os
from pathlib import Path
from omegaconf import OmegaConf

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"

class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.active_profile = os.environ.get("ACTIVE_CUSTOM_CONFIG", "customer1")
            cls._instance.config = cls._instance.load_config()
        return cls._instance
        
    def load_config(self, profile=None):
        if profile is None:
            profile = self.active_profile
        # Always reload from disk
        path = CONFIG_DIR / f"{profile}.yaml"
        if not path.exists():
            path = CONFIG_DIR / "default.yaml"
        return OmegaConf.load(path)
        
    def set_active_profile(self, profile):
        if profile in ["customer1", "customer2"]:
            self.active_profile = profile
            self.config = self.load_config()
            
    def get(self):
        # Always reload on get to ensure cross-session updates if another session modified the file
        self.config = self.load_config()
        return self.config
        
    def save(self):
        path = CONFIG_DIR / f"{self.active_profile}.yaml"
        OmegaConf.save(self.config, path)
        
    def get_remaining_usage(self) -> int:
        self.config = self.load_config()
        return int(self.config.app.get("usage_limit", 50))
        
    def decrement_usage(self) -> int:
        self.config = self.load_config()
        limit = int(self.config.app.get("usage_limit", 50))
        if limit > 0:
            self.config.app.usage_limit = limit - 1
            self.save()
            return limit - 1
        return 0
        
    def reset_to_default(self):
        default_path = CONFIG_DIR / "default.yaml"
        default_conf = OmegaConf.load(default_path)
        self.config = default_conf
        self.save()

config_manager = ConfigManager()
