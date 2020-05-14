import weakref
import aiohttp
from aiohttp import web
from app.lib.sourcesEnum import soundsEnum
import asyncio

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

    def sendToWebSocket(self):
        data = {}
        data[self.app.mashTun.name + 'TemperatureSetPoint'] = float(self.app.mashTun.getTemperatureSetPoint())
        data[self.app.mashTun.name + 'TemperatureProbe'] = float(self.app.mashTun.getTemperature())
        data[self.app.mashTun.name + 'WaterLevelSetPoint'] = float(self.app.mashTun.getWaterLevelSetPoint())
        data[self.app.mashTun.name + 'WaterLevelProbe'] = float(self.app.mashTun.getWaterLevel())
        data[self.app.mashTun.name + 'Heater'] = str(self.app.mashTun.getHeater())
        if self.app.cooking.isRunning():
            data[self.app.mashTun.name + 'TimeSetPoint'] = float(self.app.cooking.getMashTunTimeSetPoint())
            data[self.app.mashTun.name + 'TimeProbe'] = float(self.app.cooking.getMashTunTimeProbe())
        if self.app.cleaning.isRunning():
            data[self.app.mashTun.name + 'TimeSetPoint'] = float(self.app.cleaning.getMashTunTimeSetPoint())
            data[self.app.mashTun.name + 'TimeProbe'] = float(self.app.cleaning.getMashTunTimeProbe())

        data[self.app.boilKettle.name + 'TemperatureSetPoint'] = float(self.app.boilKettle.getTemperatureSetPoint())
        data[self.app.boilKettle.name + 'TemperatureProbe'] = float(self.app.boilKettle.getTemperature())
        data[self.app.boilKettle.name + 'WaterLevelSetPoint'] = float(self.app.boilKettle.getWaterLevelSetPoint())
        data[self.app.boilKettle.name + 'WaterLevelProbe'] = float(self.app.boilKettle.getWaterLevel())
        data[self.app.boilKettle.name + 'Heater'] = str(self.app.boilKettle.getHeater())
        if self.app.cooking.isRunning():
            data[self.app.boilKettle.name + 'TimeSetPoint'] = float(self.app.cooking.getBoilKettleTimeSetPoint())
            data[self.app.boilKettle.name + 'TimeProbe'] = float(self.app.cooking.getBoilKettleTimeProbe())
        if self.app.cleaning.isRunning():
            data[self.app.boilKettle.name + 'TimeSetPoint'] = float(self.app.cleaning.getBoilKettleTimeSetPoint())
            data[self.app.boilKettle.name + 'TimeProbe'] = float(self.app.cleaning.getBoilKettleTimeProbe())

        data[self.app.outletValveDump.name] = str(self.app.outletValveDump.get())
        data[self.app.chillerValveWort.name] = str(self.app.chillerValveWort.get())
        data[self.app.chillerValveWater.name] = str(self.app.chillerValveWater.get())
        data[self.app.boilKettleValveOutlet.name] = str(self.app.boilKettleValveOutlet.get())
        data[self.app.boilKettleValveInlet.name] = str(self.app.boilKettleValveInlet.get())
        data[self.app.boilKettleValveWater.name] = str(self.app.boilKettleValveWater.get())
        data[self.app.boilKettleValveReturn.name] = str(self.app.boilKettleValveReturn.get())
        data[self.app.mashTunValveOutlet.name] = str(self.app.mashTunValveOutlet.get())
        data[self.app.mashTunValveInlet.name] = str(self.app.mashTunValveInlet.get())

        data[self.app.pump.name] = str(self.app.pump.get())
        data['cookingRunning'] = str(self.app.cooking.isRunning())
        data['cleaningRunning'] = str(self.app.cleaning.isRunning())
        if self.app.cleaning.isRunning():
            data['cookingStep'] = self.app.cleaning.getCurrentStepName()
        else:
            data['cookingStep'] = self.app.cooking.getCurrentStepName()


        for log in self.getLogs():
            key = list(log)[0]
            if key not in data:
                data[key] = []
            data[key].append(log[key])
        if (len(data) > 0):
            # await self.sendJson(data)
            asyncio.run(self.sendJson(data))


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
            self.app.logger.info('[WEBSOCKET] Connection successfull')
            await self.send('connection/success')
            if not self.app.started:
                self.app.sound.play(soundsEnum.WELCOME)
                self.app.started = True
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    if msg.data == 'close':
                        await ws.close()
                    else:
                        for _ws in self._clients:
                            self.send(msg)
        except Exception as e:
            self.app.logger.exception('[WEBSOCKET] Error:', e)
        finally:
            self.app.logger.info('[WEBSOCKET] Connection closed')
            self._clients.discard(ws)

        return ws