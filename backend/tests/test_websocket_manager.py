import pytest
from api.websocket_manager import ConnectionManager

class MockWebSocket:
    def __init__(self):
        self.accepted = False
        self.closed = False
        self.close_code = None
        self.sent_messages = []

    async def accept(self):
        self.accepted = True

    async def close(self, code: int = 1000, reason: str = ""):
        self.closed = True
        self.close_code = code

    async def send_json(self, data: dict):
        self.sent_messages.append(data)


@pytest.fixture
def manager():
    return ConnectionManager()

@pytest.mark.asyncio
async def test_connect_mentor_success(manager):
    ws = MockWebSocket()
    result = await manager.connect_mentor(ws, "toby")
    assert result is True
    assert ws.accepted is True
    assert manager.rooms["toby"].active_mentor == ws

@pytest.mark.asyncio
async def test_connect_mentor_already_exists(manager):
    ws1 = MockWebSocket()
    await manager.connect_mentor(ws1, "toby")
    
    ws2 = MockWebSocket()
    result = await manager.connect_mentor(ws2, "toby")
    assert result is False
    assert ws2.accepted is True
    assert ws2.closed is True
    assert ws2.close_code == 4001
    assert "fake Mentor" in ws2.sent_messages[0]["message"]

@pytest.mark.asyncio
async def test_connect_client_success(manager):
    ws = MockWebSocket()
    result = await manager.connect_client(ws, "toby", "TestClient")
    assert result is True
    assert ws.accepted is True
    assert manager.rooms["toby"].main_client.name == "TestClient"
    assert manager.rooms["toby"].main_client.websocket == ws

@pytest.mark.asyncio
async def test_connect_client_already_exists(manager):
    ws1 = MockWebSocket()
    await manager.connect_client(ws1, "toby", "TestClient1")
    
    ws2 = MockWebSocket()
    result = await manager.connect_client(ws2, "toby", "TestClient2")
    assert result is False
    assert ws2.accepted is True
    assert ws2.closed is True
    assert ws2.close_code == 4002
    assert "someone else" in ws2.sent_messages[0]["message"]

@pytest.mark.asyncio
async def test_disconnect_and_kick(manager):
    ws_mentor = MockWebSocket()
    ws_client = MockWebSocket()
    
    await manager.connect_mentor(ws_mentor, "toby")
    await manager.connect_client(ws_client, "toby", "TestClient")
    
    assert manager.rooms["toby"].active_mentor is not None
    assert manager.rooms["toby"].main_client is not None
    
    await manager.disconnect_client("toby", ws_client)
    assert manager.rooms["toby"].main_client is None
    
    await manager.kick_mentor("toby")
    assert manager.rooms["toby"].active_mentor is None
    assert ws_mentor.closed is True
    assert ws_mentor.close_code == 4003

@pytest.mark.asyncio
async def test_multiple_rooms(manager):
    ws1 = MockWebSocket()
    ws2 = MockWebSocket()
    
    # Connect to different rooms
    await manager.connect_mentor(ws1, "toby")
    await manager.connect_mentor(ws2, "wang")
    
    assert "toby" in manager.rooms
    assert "wang" in manager.rooms
    
    # Broadcast only to toby's room
    msg = {"hello": "toby"}
    await manager.broadcast("toby", msg)
    
    assert ws1.sent_messages[-1] == msg
    assert len(ws2.sent_messages) == 0
