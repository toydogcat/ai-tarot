import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Dict, Any, List
from dotenv import set_key, load_dotenv
from omegaconf import OmegaConf
from api.websocket_manager import manager
from core.config_manager import config_manager

router = APIRouter(prefix="/api/admin", tags=["admin"])

class UsageUpdateRequest(BaseModel):
    limit: int

class RoomLevelRequest(BaseModel):
    level: str  # single, double, multi

@router.get("/rooms/status")
async def get_rooms_status():
    rooms_status = {}
    for mentor_id, room in manager.rooms.items():
        rooms_status[mentor_id] = {
            "mentor_online": room.active_mentor is not None,
            "room_level": room.room_level,
            "clients": [{"name": c.name, "is_main": c.is_main} for c in room.clients]
        }
    return {"rooms": rooms_status}

@router.get("/status")
async def get_instance_status():
    from core.db import FactorySessionLocal, mentors
    from sqlalchemy import select
    
    conf = config_manager.get()
    guide_name = conf.app.get("guide_name", "toby")
    
    rooms_list = []
    # 1. Get all registered mentors from Factory DB
    with FactorySessionLocal() as db:
        all_mentors = db.execute(select(mentors)).all()
        
    for m in all_mentors:
        mid = m.mentor_id
        room = manager.rooms.get(mid)
        
        rooms_list.append({
            "mentor_id": mid,
            "mentor_online": room.active_mentor is not None if room else False,
            "room_level": m.room_level or "single", # Priority for DB level
            "usage_limit": m.usage_limit,
            "clients": [{"name": c.name, "is_main": c.is_main} for c in room.clients] if room else []
        })
    
    # Sort: Online first, then by ID
    rooms_list.sort(key=lambda x: (not x['mentor_online'], x['mentor_id']))

    return {
        "instance_guide": guide_name,
        "rooms": rooms_list
    }

@router.post("/config/usage")
async def update_usage_limit(req: UsageUpdateRequest):
    config_manager.set_usage(req.limit)
    return {"success": True, "new_limit": req.limit}

@router.post("/rooms/{mentor_id}/usage")
async def update_mentor_usage(mentor_id: str, req: UsageUpdateRequest):
    from core.db import FactorySessionLocal, mentors
    from sqlalchemy import update
    with FactorySessionLocal() as db:
        db.execute(update(mentors).where(mentors.c.mentor_id == mentor_id).values(usage_limit=req.limit))
        db.commit()
    return {"success": True, "mentor_id": mentor_id, "new_limit": req.limit}

@router.post("/rooms/{mentor_id}/level")
async def update_room_level(mentor_id: str, req: RoomLevelRequest):
    from core.db import FactorySessionLocal, mentors
    from sqlalchemy import update
    
    # 1. Update Database (Persistence)
    with FactorySessionLocal() as db:
        db.execute(update(mentors).where(mentors.c.mentor_id == mentor_id).values(room_level=req.level))
        db.commit()
    
    # 2. Update In-Memory Room (Real-time)
    room = manager.get_room(mentor_id)
    room.room_level = req.level
    
    # 3. Enforcement (Client eviction)
    while len(room.clients) > room.max_clients:
        last_client = room.clients[-1]
        await last_client.websocket.send_json({"type": "kicked", "message": f"Room level changed to {req.level}. You have been removed."})
        await last_client.websocket.close(code=4003)
        await manager.disconnect_client(mentor_id, last_client.websocket)

    # 4. Notify everyone
    await manager.broadcast_to_clients(mentor_id, {"type": "room_update", "room_level": req.level})
    return {"success": True, "mentor_id": mentor_id, "level": req.level}

@router.post("/rooms/{mentor_id}/kick/mentor")
async def kick_mentor_by_id(mentor_id: str):
    if mentor_id in manager.rooms and manager.rooms[mentor_id].active_mentor:
        await manager.kick_mentor(mentor_id)
        return {"success": True, "message": f"Mentor {mentor_id} kicked successfully."}
    return {"success": False, "message": f"No active mentor found for {mentor_id}."}

@router.post("/rooms/{mentor_id}/kick/client")
async def kick_client_by_name(mentor_id: str, client_name: str = None):
    # If client_name is provided as query param
    if mentor_id in manager.rooms:
        await manager.kick_client(mentor_id, client_name)
        return {"success": True, "message": f"Client {client_name} kicked successfully."}
    return {"success": False, "message": f"Room {mentor_id} not found."}

@router.post("/kick_toby")
async def kick_primary_mentor():
    guide_name = config_manager.get().app.get("guide_name", "toby")
    if guide_name in manager.rooms:
        await manager.kick_mentor(guide_name)
        return {"success": True}
    return {"success": False}

@router.post("/kick_client")
async def kick_primary_client(name: str = None):
    guide_name = config_manager.get().app.get("guide_name", "toby")
    if guide_name in manager.rooms:
        await manager.kick_client(guide_name, name)
        return {"success": True}
    return {"success": False}

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
