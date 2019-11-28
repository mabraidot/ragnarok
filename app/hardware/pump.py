class pump:
    def __init__(self, app, name):
        self.app = app
        self.name = name
        self.value = False
        # Start sending the pump state to websocket
        self.app.jobs.add_job(self.sendToWebSocket, 'interval', seconds=1)
    
    def get(self):
        return self.value
    
    def set(self, newState = 'false'):
        if newState == 'true':
            self.value = True
        else:
            self.value = False
    
    async def sendToWebSocket(self):
        state = self.get()
        await self.app.ws.send(state, self.name)
