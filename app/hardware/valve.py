class valve:
    def __init__(self, app, name):
        self.app = app
        self.name = name
        self.value = 0
        # Start sending the heater state to websocket
        self.app.jobs.add_job(self.sendToWebSocket, 'interval', seconds=1)
    
    def get(self):
        return self.value
    
    def set(self, newValue = 0):
        self.value = newValue
    
    async def sendToWebSocket(self):
        state = self.get()
        await self.app.ws.send(state, self.name)
