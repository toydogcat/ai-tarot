import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from api.websocket_manager import manager

print("Active Rooms:", list(manager.rooms.keys()))
for mentor_id, room in manager.rooms.items():
    print(f"Room: {mentor_id}")
    print(f"  Active Mentor: {'ONLINE' if room.active_mentor else 'OFFLINE'}")
    print(f"  Main Client: {room.main_client.name if room.main_client else 'NONE'}")
