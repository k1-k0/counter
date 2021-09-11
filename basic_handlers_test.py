import asyncio
import pytest
from main import make_app
from basic_handlers import websockets


@pytest.fixture
def client(aiohttp_client):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(aiohttp_client(make_app()))

async def test_base_handler(client):
    resp = await client.get('/')
    assert resp.status == 200
    text = await resp.text()
    assert 'script src="base.js"' in text

async def test_increment_handler(client):
    resp = await client.get('/increment')
    assert resp.status == 200
    text = await resp.text()
    assert '1' == text

async def test_single_websocket_connect(client):
    _ = await client.ws_connect('/ws')
    assert len(websockets) == 1

async def test_multiple_websocket_connect(client):
    conn1 = await client.ws_connect('/ws')
    conn2 = await client.ws_connect('/ws')
    conn3 = await client.ws_connect('/ws')
    assert len(websockets) == 3