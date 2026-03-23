import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Dict, Any
from dotenv import set_key, load_dotenv
from omegaconf import OmegaConf
from api.websocket_manager import manager
from core.config_manager import config_manager

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/status")
async def get_status():
    conf = config_manager.get()
    app_conf = conf.app if hasattr(conf, 'app') else conf.get('app', {})
    client_name = manager.active_client[1] if manager.active_client else None
    return {
        "guide_name": app_conf.get("guide_name", "toby"),
        "toby_online": manager.active_toby is not None,
        "client_online": manager.active_client is not None,
        "client_name": client_name,
        "usage_limit": app_conf.get("usage_limit", -1)
    }

@router.post("/kick_toby")
async def kick_toby():
    if manager.active_toby:
        await manager.kick_toby()
        return {"success": True, "message": "Toby kicked successfully."}
    return {"success": False, "message": "No active Toby found."}

@router.post("/kick_client")
async def kick_client():
    if manager.active_client:
        await manager.kick_client()
        return {"success": True, "message": "Client kicked successfully."}
    return {"success": False, "message": "No active Client found."}

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "default_secret_token")
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"
CONFIG_DIR = BASE_DIR / "config"

class EnvUpdateRequest(BaseModel):
    key: str
    value: str

class YamlUpdateRequest(BaseModel):
    filename: str
    updates: Dict[str, Any]

def verify_admin(token: str):
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid Admin Token")

@router.post("/config/env")
def update_env(req: EnvUpdateRequest, admin_token: str = Header(..., alias="X-Admin-Token")):
    verify_admin(admin_token)
    try:
        if not ENV_PATH.exists():
            ENV_PATH.touch()
        set_key(str(ENV_PATH), req.key, req.value)
        load_dotenv(dotenv_path=ENV_PATH, override=True)
        return {"status": "success", "message": f"Updated {req.key} in .env successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/config/yaml")
def update_yaml_config(req: YamlUpdateRequest, admin_token: str = Header(..., alias="X-Admin-Token")):
    verify_admin(admin_token)
    yaml_path = CONFIG_DIR / req.filename
    if not yaml_path.exists():
        raise HTTPException(status_code=404, detail=f"Config file {req.filename} not found.")

    try:
        conf = OmegaConf.load(yaml_path)
        for k, v in req.updates.items():
            OmegaConf.update(conf, k, v)
        OmegaConf.save(conf, yaml_path)
        return {"status": "success", "message": f"Updated {req.filename} successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
