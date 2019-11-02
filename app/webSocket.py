import weakref
import aiohttp
from aiohttp import web

class webSocket:
    def __init__(self, app):
        self._clients = weakref.WeakSet()
        self.app = app
        self.app.add_routes([web.get('/ws', self.websocket_handler)])

    def send(self, data):
        for ws in self._clients:
            ws.send_json({'data': data})

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self._clients.add(ws)

        try:
            await ws.send_json(data=dict(topic="connection/success"))
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    if msg.data == 'close':
                        await ws.close()
                    else:
                        for _ws in self._clients:
                            _ws.send_json({'data': msg})
        finally:
            self._clients.discard(ws)

        return ws