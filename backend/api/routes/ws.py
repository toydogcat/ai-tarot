from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from api.websocket_manager import manager
from core.logger import get_logger

logger = get_logger("websocket")
router = APIRouter(tags=["websocket"])

@router.websocket("/ws/{mentor_id}/mentor")
async def websocket_mentor_endpoint(websocket: WebSocket, mentor_id: str):
    success = await manager.connect_mentor(websocket, mentor_id)
    if not success:
        return
    logger.info(f"Mentor {mentor_id} connected via WS")
    try:
        while True:
            data = await websocket.receive_json()
            logger.info(f"Mentor {mentor_id} sent data: {data}")
            # 傳給 Client
            await manager.send_to_client(mentor_id, data)
    except WebSocketDisconnect:
        await manager.disconnect_mentor(mentor_id)
        logger.info(f"Mentor {mentor_id} disconnected")

@router.websocket("/ws/{mentor_id}/client/{client_id}")
async def websocket_client_endpoint(websocket: WebSocket, mentor_id: str, client_id: str):
    success = await manager.connect_client(websocket, mentor_id, client_id)
    if not success:
        return
    logger.info(f"Client {client_id} connected to {mentor_id}'s room via WS")
    try:
        while True:
            data = await websocket.receive_json()
            logger.info(f"Client {client_id} sent data: {data}")
            data["client_name"] = client_id
            await manager.send_to_mentor(mentor_id, data)
    except WebSocketDisconnect:
        await manager.disconnect_client(mentor_id, websocket)
        logger.info(f"Client {client_id} disconnected from {mentor_id}'s room")
