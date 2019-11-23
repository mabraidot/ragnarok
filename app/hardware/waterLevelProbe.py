import random

class waterLevelProbe:
    def __init__(self, app, name = 'MashTunWaterLevelProbe'):
        self.app = app
        self.name = name
        self.value = 0
        # Start sending temperature values to websocket
        self.app.jobs.add_job(self.sendToWebSocket, 'interval', seconds=1)
    
    def get(self):
        # test value
        self.value = random.randrange(0, 16)
        return self.value
    
    async def sendToWebSocket(self):
        waterLevelValue = self.get()
        await self.app.ws.send(waterLevelValue, self.name)
