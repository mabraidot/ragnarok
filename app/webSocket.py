import weakref
import aiohttp
from aiohttp import web

class webSocket:
    def __init__(self, app):
        self.app = app
        self._clients = weakref.WeakSet()
        self.app.add_routes([web.get('/ws', self.websocket_handler)])
        self.logs = []
        self.app.jobs.add_job(self.sendToWebSocket, 'interval', seconds=1)

    def setLog(self, message):
        self.logs.append(message)

    def getLogs(self):
        messages = self.logs
        self.logs = []
        return messages

    async def sendToWebSocket(self):
        data = {}
        data[self.app.mashTun.name + 'TemperatureSetPoint'] = float(self.app.mashTun.getTemperatureSetPoint())
        data[self.app.mashTun.name + 'TemperatureProbe'] = float(self.app.mashTun.getTemperature())
        data[self.app.mashTun.name + 'WaterLevelSetPoint'] = float(self.app.mashTun.getWaterLevelSetPoint())
        data[self.app.mashTun.name + 'WaterLevelProbe'] = float(self.app.mashTun.getWaterLevel())
        data[self.app.mashTun.name + 'Heater'] = str(self.app.mashTun.getHeater())

        data[self.app.boilKettle.name + 'TemperatureSetPoint'] = float(self.app.boilKettle.getTemperatureSetPoint())
        data[self.app.boilKettle.name + 'TemperatureProbe'] = float(self.app.boilKettle.getTemperature())
        data[self.app.boilKettle.name + 'WaterLevelSetPoint'] = float(self.app.boilKettle.getWaterLevelSetPoint())
        data[self.app.boilKettle.name + 'WaterLevelProbe'] = float(self.app.boilKettle.getWaterLevel())
        data[self.app.boilKettle.name + 'Heater'] = str(self.app.boilKettle.getHeater())

        data[self.app.outletValveDump.name] = self.app.outletValveDump.get()
        data[self.app.chillerValveWort.name] = self.app.chillerValveWort.get()
        data[self.app.chillerValveWater.name] = self.app.chillerValveWater.get()
        data[self.app.boilKettleValveOutlet.name] = self.app.boilKettleValveOutlet.get()
        data[self.app.boilKettleValveInlet.name] = self.app.boilKettleValveInlet.get()
        data[self.app.boilKettleValveWater.name] = self.app.boilKettleValveWater.get()
        data[self.app.mashTunValveOutlet.name] = self.app.mashTunValveOutlet.get()
        data[self.app.mashTunValveInlet.name] = self.app.mashTunValveInlet.get()

        data[self.app.pump.name] = self.app.pump.get()

        for log in self.getLogs():
            key = list(log)[0]
            if key not in data:
                data[key] = []
            data[key].append(log[key])

        if (len(data) > 0):
            await self.sendJson(data)


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