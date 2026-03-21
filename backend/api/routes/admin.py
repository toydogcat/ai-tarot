from fastapi import APIRouter
from api.websocket_manager import manager

router = APIRouter(prefix="/api/admin", tags=["admin"])

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
