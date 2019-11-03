import random

class temperatureProbe:
    def __init__(self, app, name = 'MashTunTemperatureProbe'):
        self.app = app
        self.name = name
        self.value = 0
    
    def get(self):
        # return self.value
        temp = random.randrange(0, 100)
        return temp
    
    async def sendToWebSocket(self):
        await self.app.ws.send(self.get, self.name)
