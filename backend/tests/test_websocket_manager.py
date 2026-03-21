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
async def test_connect_toby_success(manager):
    ws = MockWebSocket()
    result = await manager.connect_toby(ws)
    assert result is True
    assert ws.accepted is True
    assert manager.active_toby == ws

@pytest.mark.asyncio
async def test_connect_toby_already_exists(manager):
    ws1 = MockWebSocket()
    await manager.connect_toby(ws1)
    
    ws2 = MockWebSocket()
    result = await manager.connect_toby(ws2)
    assert result is False
    assert ws2.accepted is True
    assert ws2.closed is True
    assert ws2.close_code == 4001
    assert "fake Toby" in ws2.sent_messages[0]["message"]

@pytest.mark.asyncio
async def test_connect_client_success(manager):
    ws = MockWebSocket()
    result = await manager.connect_client(ws, "TestClient")
    assert result is True
    assert ws.accepted is True
    assert manager.active_client == (ws, "TestClient")

@pytest.mark.asyncio
async def test_connect_client_already_exists(manager):
    ws1 = MockWebSocket()
    await manager.connect_client(ws1, "TestClient1")
    
    ws2 = MockWebSocket()
    result = await manager.connect_client(ws2, "TestClient2")
    assert result is False
    assert ws2.accepted is True
    assert ws2.closed is True
    assert ws2.close_code == 4002
    assert "someone else" in ws2.sent_messages[0]["message"]

@pytest.mark.asyncio
async def test_disconnect_and_kick(manager):
    ws_toby = MockWebSocket()
    ws_client = MockWebSocket()
    
    await manager.connect_toby(ws_toby)
    await manager.connect_client(ws_client, "TestClient")
    
    assert manager.active_toby is not None
    assert manager.active_client is not None
    
    manager.disconnect_client()
    assert manager.active_client is None
    
    await manager.kick_toby()
    assert manager.active_toby is None
    assert ws_toby.closed is True
    assert ws_toby.close_code == 4003

@pytest.mark.asyncio
async def test_broadcast(manager):
    ws_toby = MockWebSocket()
    ws_client = MockWebSocket()
    
    await manager.connect_toby(ws_toby)
    await manager.connect_client(ws_client, "Client1")
    
    msg = {"hello": "world"}
    await manager.broadcast(msg)
    
    # Check that both received the broadcast message
    assert ws_toby.sent_messages[-1] == msg
    assert ws_client.sent_messages[-1] == msg
