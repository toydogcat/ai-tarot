import os
from pathlib import Path
from omegaconf import OmegaConf
from sqlalchemy import select, update
from core.db import FactorySessionLocal, mentors

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
        
        # 1. 載入基礎預設值
        default_path = CONFIG_DIR / "default.yaml"
        config = OmegaConf.load(default_path)
        
        # 2. 若非預設檔，則進行合併 (覆寫模式)
        if profile != "default":
            path = CONFIG_DIR / f"{profile}.yaml"
            if path.exists():
                override_config = OmegaConf.load(path)
                config = OmegaConf.merge(config, override_config)
            else:
                # 若檔案不存在，則視為使用預設
                pass
        return config
        
    def get(self):
        self.config = self.load_config()
        return self.config
        
    def save(self):
        path = CONFIG_DIR / f"{self.active_profile}.yaml"
        OmegaConf.save(self.config, path)
        
    def get_remaining_usage(self) -> int:
        """從全局 Factory DB 讀取導師剩餘次數 (優先於 YAML)"""
        conf = self.get()
        mentor_id = conf.app.get("guide_name", "toby")
        
        with FactorySessionLocal() as db:
            mentor = db.execute(select(mentors).where(mentors.c.mentor_id == mentor_id)).first()
            if mentor:
                return mentor.usage_limit
        return int(conf.app.get("usage_limit", 5))

    def set_usage(self, limit: int):
        """同步更新 YAML 與 Factory DB 中的使用次數"""
        self.config = self.load_config()
        self.config.app.usage_limit = limit
        self.save()
        
        mentor_id = self.config.app.get("guide_name", "toby")
        with FactorySessionLocal() as db:
            db.execute(update(mentors).where(mentors.c.mentor_id == mentor_id).values(usage_limit=limit))
            db.commit()
            
    def reset_to_default(self):
        default_path = CONFIG_DIR / "default.yaml"
        default_conf = OmegaConf.load(default_path)
        self.config = default_conf
        self.save()

config_manager = ConfigManager()
