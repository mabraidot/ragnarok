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
        self.app.jobs.add_job(self.timerHeating, 'interval', seconds=1, id=name+'Heating')
        self.temperatureSetPoint = 0.0
        self.waterLevelProbe = waterLevelProbe(app, self.config, self.name + 'WaterLevelProbe')
        self.waterSetPoint = 0.0
        self.heater = heater(app, self.config, self.name + 'Heater')

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
        self.heater.set(newState)

    def getPWM(self):
        return self.heater.getPWM()

    def setPWM(self, newPWM = 0):
        self.heater.setPWM(newPWM)




    def timerHeating(self):
        if self.getTemperatureSetPoint() > 0 and not self.PIDAutoTune.running:
            if self.getWaterLevel() >= self.config.getfloat('SAFE_WATER_LEVEL_FOR_HEATERS'):
                self.heater.pid(self.getTemperatureSetPoint(), self.getTemperature())
                if not self.getHeater():
                    self.setHeater('true')
            else:
                self.setHeater('false')

            # Safety measure, if termperature raises 10 degrees over setpoint, shut down the heater
            # if self.getTemperature() >= self.getTemperatureSetPoint() + self.config.getfloat('SAFE_OVERHEAT_TEMPERATURE'):
            #     self.setHeater('false')
        # elif self.getHeater() and not self.PIDAutoTune.running:
            # self.setHeater('false')
        # if self.getWaterLevel() < self.config.getfloat('SAFE_WATER_LEVEL_FOR_HEATERS'):
        #     self.setHeater('false')



    def heatToTemperature(self, temperature = 0):
        self.temperatureSetPoint = float(temperature)
        if self.getTemperature() < self.temperatureSetPoint:
            self.setHeater('true')

    def stopHeating(self):
        self.temperatureSetPoint = 0
        self.setHeater('false')
