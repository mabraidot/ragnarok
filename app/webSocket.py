import weakref
import aiohttp
from aiohttp import web

class webSocket:
    def __init__(self, app):
        self._clients = weakref.WeakSet()
        app.add_routes([web.get('/ws', self.websocket_handler)])

    async def send(self, data, topic = 'data'):
        for ws in self._clients:
            await ws.send_json({topic: data})

    async def sendJson(self, jsonData):
        for ws in self._clients:
            await ws.send_json(jsonData)

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self._clients.add(ws)

        try:
            await self.send('connection/success')
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    if msg.data == 'close':
                        await ws.close()
                    else:
                        for _ws in self._clients:
                            self.send(msg)
        finally:
            self._clients.discard(ws)

        return ws