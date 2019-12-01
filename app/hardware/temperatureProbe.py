import random

class temperatureProbe:
    def __init__(self, app, name = 'MashTunTemperatureProbe'):
        self.app = app
        self.name = name
        self.value = 0
        # Start sending water level values to websocket
        # self.app.jobs.add_job(self.sendToWebSocket, 'interval', seconds=1)
    
    def get(self):
        # @TODO: this is a TEST. Restore the actual value
        # self.value = random.randrange(0, 110)
        if self.app.mashTun.getHeater() and self.value < 110:
            self.value += 1
        elif self.value > 0:
            self.value -= 0.1

        return self.value
    
    async def sendToWebSocket(self):
        tempValue = self.get()
        await self.app.ws.send(tempValue, self.name)
