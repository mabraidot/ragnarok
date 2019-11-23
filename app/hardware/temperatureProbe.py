import random

class temperatureProbe:
    def __init__(self, app, name = 'MashTunTemperatureProbe'):
        self.app = app
        self.name = name
        self.value = 0
        # Start sending water level values to websocket
        self.app.jobs.add_job(self.sendToWebSocket, 'interval', seconds=1)
    
    def get(self):
        # test value
        self.value = random.randrange(0, 110)
        return self.value
    
    async def sendToWebSocket(self):
        tempValue = self.get()
        await self.app.ws.send(tempValue, self.name)
