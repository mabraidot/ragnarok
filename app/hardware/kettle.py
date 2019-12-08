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

        self.temperatureProbe = temperatureProbe(app, self.name + 'TemperatureProbe')
        self.temperatureSetPoint = 0.0
        self.waterLevelProbe = waterLevelProbe(app, self.name + 'WaterLevelProbe')
        self.waterSetPoint = 0.0
        self.heater = heater(app, self.config['HEATER'], self.name + 'Heater')
        
    def getTemperature(self):
        return self.temperatureProbe.get()
    
    def setTemperature(self, newValue = 0):
        self.temperatureSetPoint = float(newValue)
    
    def getTemperatureSetPoint(self):
        return self.temperatureSetPoint
    
    def getWaterLevel(self):
        currentLevel = self.waterLevelProbe.get()
        # @TODO: restore this safety water level condition
        # if currentLevel < self.config.getfloat('SAFE_WATER_LEVEL_FOR_HEATERS'):
        #     self.setHeater('false')
        return currentLevel
    
    def setWaterLevel(self, newValue = 0):
        self.waterSetPoint = float(newValue)
    
    def getWaterLevelSetPoint(self):
        return self.waterSetPoint

    def getHeater(self):
        return self.heater.get()
    
    def setHeater(self, newState = 'false'):
        # @TODO: restore this safety water level condition
        # if newState == 'true' and self.getWaterLevel() >= self.config.getfloat('SAFE_WATER_LEVEL_FOR_HEATERS'):
        if newState == 'true':
            self.heater.set('true')
        else:
            self.heater.set('false')
