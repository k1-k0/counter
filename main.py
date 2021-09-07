from aiohttp import web
import aiohttp

counter = 0
websockets = []

async def base_handle(request):
    return web.FileResponse('index.html')

async def increment_handle(request):
    global counter
    counter += 1
    return web.Response(text=str(counter))

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

    print('websocket closed')
    websockets.remove(ws)

    return ws

async def js_handle(request):
    return web.FileResponse('base.js')

app = web.Application()
app.add_routes([
    web.get('/', handler=base_handle),
    web.get('/increment', handler=increment_handle),
    web.get('/ws', handler=ws_handle),
    web.get('/base.js', handler=js_handle),
    ])

if __name__ == '__main__':
    web.run_app(app=app)
