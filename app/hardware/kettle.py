from app.hardware.temperatureProbe import temperatureProbe
from app.hardware.waterLevelProbe import waterLevelProbe
from app.hardware.heater import heater

class kettle:
    def __init__(self, app, name = 'MashTun'):
        self.app = app
        self.name = name

        self.temperatureProbe = temperatureProbe(app, self.name + 'TemperatureProbe')
        self.temperatureSetPoint = 0
        self.waterLevelProbe = waterLevelProbe(app, self.name + 'WaterLevelProbe')
        self.waterSetPoint = 0
        self.heater = heater(app, self.name + 'Heater')
        
        # Start sending all the values to websocket
        self.app.jobs.add_job(self.sendToWebSocket, 'interval', seconds=1)
    
    def getTemperature(self):
        return self.temperatureProbe.get()
    
    def setTemperature(self, newValue = 0):
        self.temperatureSetPoint = float(newValue)
    
    def getWaterLevel(self):
        return self.waterLevelProbe.get()
    
    def setWaterLevel(self, newValue = 0):
        self.waterSetPoint = float(newValue)
    
    def getHeater(self):
        return self.heater.get()
    
    def setHeater(self, newState = 'false'):
        self.heater.set(newState)
    
    async def sendToWebSocket(self):
        data = {}
        data[self.name + 'TemperatureProbe'] = self.getTemperature()
        data[self.name + 'WaterLevelProbe'] = self.getWaterLevel()
        data[self.name + 'Heater'] = self.getHeater()
        
        await self.app.ws.sendJson(data)
