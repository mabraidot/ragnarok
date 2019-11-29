class heater:
    def __init__(self, app, pin, name = 'MashTunHeater'):
        self.app = app
        self.name = name
        self.pin = pin
        self.value = False
        self.pwm = 0
        # Start sending the heater state to websocket
        # self.app.jobs.add_job(self.sendToWebSocket, 'interval', seconds=1)
    
    def get(self):
        return self.value
    
    def set(self, newState = 'false'):
        if newState == 'true':
            self.value = True
        else:
            self.value = False
    
    async def sendToWebSocket(self):
        state = self.get()
        await self.app.ws.send(str(state), self.name)
