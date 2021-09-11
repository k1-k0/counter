import aiohttp
from aiohttp import web

counter = 0 
websockets = []

basic_routes = web.RouteTableDef()

@basic_routes.get('/')
async def base_handle(request):
    return web.FileResponse('./static/index.html')

@basic_routes.get('/increment')
async def increment_handle(request):
    global counter
    counter += 1
    return web.Response(text=str(counter))

@basic_routes.get('/ws')
async def ws_handle(request):
    global websockets

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    websockets.append(ws)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                for _ws in websockets:
                    await _ws.send_str(str(counter))
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('websocket connection closed with exception %s', ws.exception())

    websockets.remove(ws)

    return ws
