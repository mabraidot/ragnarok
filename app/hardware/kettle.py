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
        self.app.jobs.add_job(self.timerHeating, 'interval', seconds=1)
        self.temperatureSetPoint = 0.0
        self.waterLevelProbe = waterLevelProbe(app, self.config, self.name + 'WaterLevelProbe')
        self.app.jobs.add_job(self.timerWaterLevel, 'interval', seconds=1)
        self.waterSetPoint = 0.0
        self.heater = heater(app, self.config['HEATER'], self.name + 'Heater')

    def getTemperature(self):
        return self.temperatureProbe.get()

    def setTemperature(self, newValue = 0):
        self.temperatureSetPoint = float(newValue)

    def getTemperatureSetPoint(self):
        return self.temperatureSetPoint

    def getWaterLevel(self):
        return self.waterLevelProbe.get()

    def setWaterLevel(self, newValue = 0):
        self.waterSetPoint = min(float(newValue), self.config.getfloat('MAX_WATER_LEVEL'))

    def getWaterLevelSetPoint(self):
        return self.waterSetPoint

    def getHeater(self):
        return self.heater.get()

    def setHeater(self, newState = 'false'):
        if newState == 'true' and self.getWaterLevel() >= self.config.getfloat('SAFE_WATER_LEVEL_FOR_HEATERS'):
            self.heater.set('true')
        else:
            self.heater.set('false')



    def timerHeating(self):
        if self.getTemperatureSetPoint() > 0 and self.getHeater():
            # TODO: set timer to heat using PID. Heater on for testing
            self.setHeater('true')

        # Safety measure, if termperature raises 10 degrees over setpoint, shut down the heater
        if self.temperatureProbe.get() >= self.getTemperatureSetPoint() + 10:
                self.setHeater('false')

    def timerWaterLevel(self):
        # Safety measure, if water level is greater than setpoint, shut down the pump
        if self.getWaterLevelSetPoint() > 0 and self.getWaterLevel() >= self.getWaterLevelSetPoint():
            self.app.pump.set('false')


    def heatToTemperature(self, temperature = 0):
        self.temperatureSetPoint = float(temperature)
        if self.getTemperature() < self.temperatureSetPoint:
            self.setHeater("true")
        else:
            self.setHeater("false")
