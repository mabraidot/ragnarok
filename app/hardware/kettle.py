from app.hardware.temperatureProbe import temperatureProbe
from app.hardware.waterLevelProbe import waterLevelProbe
from app.hardware.heater import heater
from app.hardware.PIDAutoTune import PIDAutoTune

class kettle:
    def __init__(self, app, config, name = 'MashTun'):
        self.app = app
        self.name = name
        self.config = config
        self.PIDAutoTune = PIDAutoTune(self.app, self, self.config)
        self.log = []

        self.temperatureProbe = temperatureProbe(app, self.name + 'TemperatureProbe')
        self.temperatureSetPoint = 0
        self.waterLevelProbe = waterLevelProbe(app, self.name + 'WaterLevelProbe')
        self.waterSetPoint = 0
        self.heater = heater(app, self.config['HEATER'], self.name + 'Heater')
        
        # Start sending all the values to websocket
        self.app.jobs.add_job(self.sendToWebSocket, 'interval', seconds=1)
    
    def getTemperature(self):
        return self.temperatureProbe.get()
    
    def setTemperature(self, newValue = 0):
        self.temperatureSetPoint = float(newValue)
    
    def getTemperatureSetPoint(self):
        return self.temperatureSetPoint
    
    def getWaterLevel(self):
        currentLevel = self.waterLevelProbe.get()
        if currentLevel < self.config.getfloat('SAFE_WATER_LEVEL_FOR_HEATERS'):
            self.setHeater('false')
        return currentLevel
    
    def setWaterLevel(self, newValue = 0):
        self.waterSetPoint = float(newValue)
    
    def getWaterLevelSetPoint(self):
        return self.waterSetPoint

    def getHeater(self):
        return self.heater.get()
    
    def setHeater(self, newState = 'false'):
        if newState == 'true' and self.getWaterLevel() >= self.config.getfloat('SAFE_WATER_LEVEL_FOR_HEATERS'):
            self.heater.set(newState)
        else:
            self.heater.set('false')
    
    def setLog(self, message = ''):
        self.log.append(message)

    def getLog(self):
        messages = self.log
        self.log = []
        return messages
    
    async def sendToWebSocket(self):
        data = {}
        data[self.name + 'TemperatureSetPoint'] = self.getTemperatureSetPoint()
        data[self.name + 'TemperatureProbe'] = self.getTemperature()
        data[self.name + 'WaterLevelSetPoint'] = self.getWaterLevelSetPoint()
        data[self.name + 'WaterLevelProbe'] = self.getWaterLevel()
        data[self.name + 'Heater'] = str(self.getHeater())
        data['log'] = self.getLog()
        
        await self.app.ws.sendJson(data)
