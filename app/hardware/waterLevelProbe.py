from RPi import GPIO
from app.lib.hx711 import HX711
import random
import threading
import time

class waterLevelProbe:
    def __init__(self, app, config, name = 'MashTunWaterLevelProbe'):
        self.app = app
        self.name = name
        self.config = config
        self.value = 0
        self.runningTare = False

        if self.config.get('ENVIRONMENT') == 'production':
            # https://github.com/tatobari/hx711py/blob/master/example.py
            # https://tutorials-raspberrypi.com/digital-raspberry-pi-scale-weight-sensor-hx711/
            self.hx = HX711(self.config.getint('WATER_LEVEL_SENSOR_DT'), self.config.getint('WATER_LEVEL_SENSOR_SCK'))
            self.hx.set_reading_format("MSB", "MSB")
            self.hx.set_reference_unit(self.config.getfloat('WATER_LEVEL_SENSOR_REFERENCE_UNIT'))
            
            tare = threading.Thread(target=self.runTare)
            tare.start()

            task = threading.Thread(target=self.run)
            task.start()


    def tare(self):
        # tare = threading.Thread(target=self.runTare)
        # tare.start()
        if self.config.get('ENVIRONMENT') == 'production':
            self.runningTare = True
            self.hx.reset()
            self.hx.tare()
            self.runningTare = False


    def runTare(self):
        if self.config.get('ENVIRONMENT') == 'production':
            self.runningTare = True
            self.hx.reset()
            self.hx.tare()
            self.runningTare = False

    def setPriorValue(self, value):
        if self.config.get('ENVIRONMENT') == 'production':
            # offsetTask = threading.Thread(target=self.runPriorValue, kwargs=dict(value=value))
            # offsetTask.start()
            newValue = -1 * (value * self.config.getfloat('ONE_LITER_WEIGHT')) * 1000
            self.hx.reset()
            self.hx.set_offset(self.hx.get_offset() + (newValue * self.config.getfloat('WATER_LEVEL_SENSOR_REFERENCE_UNIT')))
        else:
            self.value = (value * self.config.getfloat('ONE_LITER_WEIGHT')) * 1000

    def runPriorValue(self, value):
        self.runningTare = True
        newValue = -1 * (value * self.config.getfloat('ONE_LITER_WEIGHT')) * 1000
        self.hx.reset()
        self.hx.set_offset(self.hx.get_offset() + (newValue * self.config.getfloat('WATER_LEVEL_SENSOR_REFERENCE_UNIT')))
        self.runningTare = False


    def get(self):
        if self.config.get('ENVIRONMENT') == 'development':
            flow = 200
            if self.name == 'MashTunWaterLevelProbe':
                if self.app.pump.get():
                    inletValveState = self.app.mashTunValveInlet.get()
                    outletValveState = self.app.mashTunValveOutlet.get()
                    if inletValveState > 0:
                        self.value += flow
                    if outletValveState > 0:
                        if self.value > flow:
                            self.value -= flow
                        else:
                            self.value = 0

            else:
                inletValveState = self.app.boilKettleValveInlet.get()
                waterValveState = self.app.boilKettleValveWater.get()
                if inletValveState > 0 or waterValveState > 0:
                    self.value += flow
                elif self.app.pump.get():
                    returnValveState = self.app.boilKettleValveReturn.get()
                    outletValveState = self.app.boilKettleValveOutlet.get()
                    if returnValveState > 0:
                        self.value += flow
                    if outletValveState > 0:
                        if self.value > flow:
                            self.value -= flow
                        else:
                            self.value = 0
        currentLevel = ( self.value / 1000 ) / self.config.getfloat('ONE_LITER_WEIGHT')
        if self.name == 'MashTunWaterLevelProbe':
            currentTemperature = self.app.mashTun.getTemperature()
        else:
            currentTemperature = self.app.boilKettle.getTemperature()
        if currentTemperature > 25 and self.config.get('ENVIRONMENT') == 'production':
            currentLevel -= (2 / 50) * (currentTemperature - 25)
        return currentLevel


    def run(self):
        try:
            while True:
                if not self.runningTare:
                    oldValue = self.value
                    newValue = self.hx.get_weight(5)
                    if oldValue - newValue > -2000:
                        self.value = newValue
                        if self.value < 0:
                            self.value = 0

                    self.hx.reset()
                    time.sleep(0.5)
        except:
            GPIO.cleanup()