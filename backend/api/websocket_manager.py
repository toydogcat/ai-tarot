from fastapi import WebSocket
from typing import List, Optional, Tuple

class ClientInfo:
    def __init__(self, websocket: WebSocket, name: str, is_main: bool = False):
        self.websocket = websocket
        self.name = name
        self.is_main = is_main

class Room:
    def __init__(self, mentor_id: str):
        self.mentor_id = mentor_id
        self.active_mentor: Optional[WebSocket] = None
        self.clients: List[ClientInfo] = []
        self.room_level: str = "single"  # single, double, multi
        self.max_clients_override: Optional[int] = None
        self.announcement: str = ""
        self.ai_enabled: bool = True

    @property
    def max_clients(self) -> int:
        if self.max_clients_override is not None:
            return self.max_clients_override
            
        if self.room_level == "multi":
            return 4
        if self.room_level == "double":
            return 1
        return 0  # single

    @property
    def main_client(self) -> Optional[ClientInfo]:
        for c in self.clients:
            if c.is_main:
                return c
        return None

class ConnectionManager:
    def __init__(self):
        self.rooms: dict[str, Room] = {}

    def get_room(self, mentor_id: str) -> Room:
        if mentor_id not in self.rooms:
            room = Room(mentor_id)
            # Pre-load settings from DB to avoid state flickering
            from core.db import FactorySessionLocal, mentors
            from sqlalchemy import select
            try:
                with FactorySessionLocal() as db:
                    m_row = db.execute(select(mentors).where(mentors.c.mentor_id == mentor_id)).first()
                    if m_row:
                        room.room_level = m_row.room_level or "single"
                        room.max_clients_override = m_row.max_clients
                        room.announcement = m_row.announcement or ""
                        room.ai_enabled = m_row.ai_enabled if m_row.ai_enabled is not None else True
            except Exception:
                pass # Fallback to defaults
            self.rooms[mentor_id] = room
        return self.rooms[mentor_id]

    async def connect_mentor(self, websocket: WebSocket, mentor_id: str) -> bool:
        await websocket.accept()
        room = self.get_room(mentor_id)
        
        # Load room settings from DB
        from core.db import FactorySessionLocal, mentors
        from sqlalchemy import select
        with FactorySessionLocal() as db:
            mentor_row = db.execute(select(mentors).where(mentors.c.mentor_id == mentor_id)).first()
            if mentor_row:
                room.room_level = mentor_row.room_level
                room.max_clients_override = mentor_row.max_clients
                room.announcement = mentor_row.announcement or ""
                room.ai_enabled = mentor_row.ai_enabled if mentor_row.ai_enabled is not None else True
        
        # If an old mentor WS is still connected, gracefully close it (e.g. page refresh)
        if room.active_mentor is not None:
            try:
                await room.active_mentor.close(code=4000)
            except Exception:
                pass  # Old connection already dead
            room.active_mentor = None
            
        room.active_mentor = websocket
        
        # Notify mentor about current clients
        if room.clients:
            await self.send_to_mentor(mentor_id, {
                "type": "clients_list", 
                "clients": [{"name": c.name, "is_main": c.is_main} for c in room.clients]
            })
            
        await self.broadcast_mentor_presence(mentor_id, True)
        # Notify already-connected clients that mentor is now online
        await self.broadcast_to_clients(mentor_id, {"type": "toby_status", "is_online": True})
        return True

    async def connect_client(self, websocket: WebSocket, mentor_id: str, client_name: str) -> bool:
        await websocket.accept()
        room = self.get_room(mentor_id)
        
        # Check for existing session with same name (Reconnection/Refresh)
        existing_client = next((c for c in room.clients if c.name == client_name), None)
        if existing_client:
            try:
                await existing_client.websocket.close(code=4000)
            except Exception:
                pass
            room.clients.remove(existing_client)
        
        if len(room.clients) >= room.max_clients:
            await websocket.send_json({"type": "error", "message": f"Room is full (Level: {room.room_level})"})
            await websocket.close(code=4002)
            return False
            
        # First client in room becomes Main Client
        is_main = (room.main_client is None)
        client = ClientInfo(websocket, client_name, is_main)
        room.clients.append(client)
        
        # Notify Client about their status
        await websocket.send_json({
            "type": "room_init",
            "is_main": is_main,
            "room_level": room.room_level,
            "toby_online": room.active_mentor is not None,
            "announcement": room.announcement
        })
        
        # Notify Mentor
        await self.send_to_mentor(mentor_id, {
            "type": "client_connected", 
            "client_name": client_name,
            "is_main": is_main
        })
        
        return True

    async def disconnect_mentor(self, mentor_id: str):
        room = self.rooms.get(mentor_id)
        if room and room.active_mentor:
            room.active_mentor = None
            await self.broadcast_to_clients(mentor_id, {"type": "toby_status", "is_online": False})
            await self.broadcast_mentor_presence(mentor_id, False)
            
    async def disconnect_client(self, mentor_id: str, websocket: WebSocket):
        room = self.rooms.get(mentor_id)
        if room:
            # Find and remove client
            client_to_remove = None
            for c in room.clients:
                if c.websocket == websocket:
                    client_to_remove = c
                    break
            
            if client_to_remove:
                room.clients.remove(client_to_remove)
                # If main client left, assign new main client from remaining
                if client_to_remove.is_main and room.clients:
                    room.clients[0].is_main = True
                    # Notify the new main client
                    await room.clients[0].websocket.send_json({"type": "role_upgrade", "is_main": True})
                
                # Notify mentor
                await self.send_to_mentor(mentor_id, {
                    "type": "client_disconnected", 
                    "client_name": client_to_remove.name
                })
            
    async def kick_mentor(self, mentor_id: str):
        room = self.rooms.get(mentor_id)
        if room and room.active_mentor:
            await room.active_mentor.send_json({"type": "kicked", "message": "You have been kicked by the admin."})
            await room.active_mentor.close(code=4003)
            room.active_mentor = None
            
    async def kick_client(self, mentor_id: str, client_name: Optional[str] = None):
        room = self.rooms.get(mentor_id)
        if not room: return
        
        to_kick = []
        if client_name:
            to_kick = [c for c in room.clients if c.name == client_name]
        else:
            # Legacy: kick main client
            main = room.main_client
            if main: to_kick = [main]
            
        for c in to_kick:
            await c.websocket.send_json({"type": "kicked", "message": "You have been kicked by the admin."})
            await c.websocket.close(code=4003)
            await self.disconnect_client(mentor_id, c.websocket)

    async def send_to_mentor(self, mentor_id: str, message: dict):
        room = self.rooms.get(mentor_id)
        if room and room.active_mentor:
            try:
                await room.active_mentor.send_json(message)
            except Exception:
                await self.disconnect_mentor(mentor_id)

    async def broadcast_to_clients(self, mentor_id: str, message: dict):
        room = self.rooms.get(mentor_id)
        if room:
            for c in room.clients:
                try:
                    await c.websocket.send_json(message)
                except Exception:
                    pass # Disconnect will be handled by ws.on_disconnect

    async def broadcast(self, mentor_id: str, message: dict):
        await self.send_to_mentor(mentor_id, message)
        await self.broadcast_to_clients(mentor_id, message)

    async def broadcast_mentor_presence(self, mentor_id: str, is_online: bool):
        from core.db import FactorySessionLocal, mentor_friends
        from sqlalchemy import or_, and_, select
        import asyncio
        
        def get_friends():
            with FactorySessionLocal() as db:
                links = db.execute(select(mentor_friends).where(
                    and_(
                        or_(mentor_friends.c.requester_id == mentor_id, mentor_friends.c.receiver_id == mentor_id),
                        mentor_friends.c.status == 'accepted'
                    )
                )).fetchall()
                
            friends = []
            for link in links:
                friends.append(link.receiver_id if link.requester_id == mentor_id else link.requester_id)
            return friends
            
        friends = await asyncio.to_thread(get_friends)
        
        for friend_id in friends:
            room = self.rooms.get(friend_id)
            if room and room.active_mentor:
                try:
                    await room.active_mentor.send_json({
                        "type": "friend_presence",
                        "mentor_id": mentor_id,
                        "is_online": is_online
                    })
                except Exception:
                    pass

    async def broadcast_announcement(self, mentor_id: str, text: str):
        room = self.rooms.get(mentor_id)
        if room:
            room.announcement = text
            await self.broadcast(mentor_id, {
                "type": "announcement_update",
                "text": text
            })

manager = ConnectionManager()
