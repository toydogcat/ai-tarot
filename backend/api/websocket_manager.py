from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # 整個系統只有一個 Toby 和一個 Client 的連線
        self.active_toby: WebSocket | None = None
        self.active_client: tuple[WebSocket, str] | None = None  # (WebSocket, client_name)

    async def connect_toby(self, websocket: WebSocket) -> bool:
        """
        嘗試連接 Toby。如果已經有 Toby 在線上，則拒絕連線。
        Returns True if successful, False if rejected.
        """
        await websocket.accept()
        if self.active_toby is not None:
            # 已經有 Toby 了，拒絕
            await websocket.send_json({"type": "error", "message": "You are a fake Toby. A Toby is already online."})
            await websocket.close(code=4001)
            return False
        
        self.active_toby = websocket
        # 若目前有 Client，通知 Toby 當前 Client是誰
        if self.active_client:
            _, client_name = self.active_client
            await self.send_to_toby({"type": "client_connected", "client_name": client_name})
            await self.send_to_client({"type": "toby_status", "is_online": True})
        return True

    async def connect_client(self, websocket: WebSocket, client_name: str) -> bool:
        """
        嘗試連接 Client。如果已經有 Client 在線上，則拒絕連線。
        Returns True if successful, False if rejected.
        """
        await websocket.accept()
        if self.active_client is not None:
            # 已經有 Client 了，拒絕
            await websocket.send_json({"type": "error", "message": "Please wait, someone else is getting a reading."})
            await websocket.close(code=4002)
            return False
        
        self.active_client = (websocket, client_name)
        # 通知 Toby 有新 Client 進來了
        await self.send_to_toby({"type": "client_connected", "client_name": client_name})
        # 通知 Client 目前 Toby 的狀態
        is_toby_online = self.active_toby is not None
        await self.send_to_client({"type": "toby_status", "is_online": is_toby_online})
        return True

    async def disconnect_toby(self):
        if self.active_toby:
            self.active_toby = None
            await self.send_to_client({"type": "toby_status", "is_online": False})
            
    def disconnect_client(self):
        if self.active_client:
            self.active_client = None
            
    async def kick_toby(self):
        if self.active_toby:
            await self.active_toby.send_json({"type": "kicked", "message": "You have been kicked by the admin."})
            await self.active_toby.close(code=4003)
            self.active_toby = None
            
    async def kick_client(self):
        if self.active_client:
            ws, _ = self.active_client
            await ws.send_json({"type": "kicked", "message": "You have been kicked by the admin."})
            await ws.close(code=4003)
            self.active_client = None

    async def send_to_toby(self, message: dict):
        """傳送訊息給 Toby"""
        print(f"DEBUG: Attempting to send message to Toby. active_toby exists? {self.active_toby is not None}")
        if self.active_toby:
            try:
                await self.active_toby.send_json(message)
                print("DEBUG: Message sent to Toby successfully")
            except Exception as e:
                print(f"DEBUG: Error sending to Toby: {e}")
                import asyncio
                asyncio.create_task(self.disconnect_toby())

    async def send_to_client(self, message: dict):
        """傳送訊息給目前的 Client"""
        if self.active_client:
            ws, _ = self.active_client
            try:
                await ws.send_json(message)
            except Exception:
                self.disconnect_client()

    async def broadcast(self, message: dict):
        """傳送給雙方"""
        await self.send_to_toby(message)
        await self.send_to_client(message)

# 建立全局單例 manager
manager = ConnectionManager()
