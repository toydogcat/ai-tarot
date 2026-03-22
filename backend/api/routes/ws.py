from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from api.websocket_manager import manager
from core.logger import get_logger

logger = get_logger("websocket")
router = APIRouter(tags=["websocket"])

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    if client_id.lower() == "toby":
        success = await manager.connect_toby(websocket)
        if not success:
            return
        logger.info("Toby connected via WS")
        try:
            while True:
                data = await websocket.receive_json()
                logger.info(f"Toby sent data: {data}")
                # 收到 Toby 傳來的對話或狀態更新，直接轉發給 Client
                await manager.send_to_client(data)
        except WebSocketDisconnect:
            await manager.disconnect_toby()
            logger.info("Toby disconnected")
    else:
        success = await manager.connect_client(websocket, client_id)
        if not success:
            return
        logger.info(f"Client {client_id} connected via WS")
        try:
            while True:
                data = await websocket.receive_json()
                logger.info(f"Client {client_id} sent data: {data}")
                # 收到 Client 傳來的對話或狀態更新，加上 client_name 轉發給 Toby
                data["client_name"] = client_id
                await manager.send_to_toby(data)
        except WebSocketDisconnect:
            manager.disconnect_client()
            logger.info(f"Client {client_id} disconnected")
