from RPi import GPIO
from app.lib.hx711 import HX711
import random
import threading
import time

# Temperature compensation
# Wcomp = Wraw*(1−c*(Tcal−Tsc))
# Wraw : raw weight values from scale
# c : compensation coefficient (I use 0.0002 for the same scale/ADC setup)
# Tcal : Temperature at calibration time (around 25°C)
# Tsc : Temperature of scale (put the sensor close to the scale)


class waterLevelProbe:
    def __init__(self, app, config, name = 'MashTunWaterLevelProbe'):
        self.app = app
        self.name = name
        self.config = config
        self.value = -1000
        self.runningTare = True

        try:
            if self.config.get('ENVIRONMENT') == 'production':
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(self.config.getint('WATER_LEVEL_SENSOR_DT'), GPIO.IN)
                GPIO.setup(self.config.getint('WATER_LEVEL_SENSOR_SCK'), GPIO.OUT)
                # https://github.com/tatobari/hx711py/blob/master/example.py
                # https://tutorials-raspberrypi.com/digital-raspberry-pi-scale-weight-sensor-hx711/
                self.hx = HX711(self.config.getint('WATER_LEVEL_SENSOR_DT'), self.config.getint('WATER_LEVEL_SENSOR_SCK'))
                self.hx.set_reading_format("MSB", "MSB")
                self.hx.set_reference_unit(self.config.getfloat('WATER_LEVEL_SENSOR_REFERENCE_UNIT'))
                
                tare = threading.Thread(target=self.runTare)
                tare.start()

                task = threading.Thread(target=self.run)
                task.start()

            else:
                self.app.jobs.add_job(self.waterDaemon, 'interval', seconds=0.5, id='waterDaemon'+self.name, replace_existing=True)
                tare = threading.Thread(target=self.runTare)
                tare.start()

        except Exception as e:
            self.app.logger.exception(e)


    def waterDaemon(self):
        if self.config.get('ENVIRONMENT') == 'development':
            flow = 100
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
                    chillerValveState = self.app.chillerValveWort.get()
                    if returnValveState > 0 or chillerValveState > 0:
                        self.value += flow
                    if outletValveState > 0:
                        if self.value > flow:
                            self.value -= flow
                        else:
                            self.value = 0


    def tare(self):
        if self.config.get('ENVIRONMENT') == 'production':
            while not self.hx.is_ready():
                pass
            self.value = -1000
            self.runningTare = True
            self.hx.reset()
            self.hx.tare()
            self.value = 0
            self.runningTare = False
        else:
            self.value = 0
            self.runningTare = False


    def runTare(self):
        try:
            self.app.logger.info('Running Tare %s', self.name)
            if self.config.get('ENVIRONMENT') == 'production':
                while not self.hx.is_ready():
                    pass
                self.value = -1000
                self.runningTare = True
                self.hx.reset()
                self.hx.tare()
                self.value = 0
                self.runningTare = False
            else:
                self.value = 0
                self.runningTare = False
        except Exception as e:
            self.app.logger.exception(e)


    def setPriorValue(self, value):
        if self.config.get('ENVIRONMENT') == 'production':
            newValue = -1 * (value * self.config.getfloat('ONE_LITER_WEIGHT')) * 1000
            self.hx.reset()
            self.hx.set_offset(self.hx.get_offset() + (newValue * self.config.getfloat('WATER_LEVEL_SENSOR_REFERENCE_UNIT')))
        else:
            self.value = (value * self.config.getfloat('ONE_LITER_WEIGHT')) * 1000


    def get(self):
        currentLevel = ( self.value / 1000 ) / self.config.getfloat('ONE_LITER_WEIGHT')
        # if self.name == 'MashTunWaterLevelProbe':
        #     currentTemperature = self.app.mashTun.getTemperature()
        # else:
        #     currentTemperature = self.app.boilKettle.getTemperature()

        # if currentTemperature > 25 and self.config.get('ENVIRONMENT') == 'production':
        #     currentLevel -= (0.8 / 50) * (currentTemperature - 25)
        return currentLevel


    def run(self):
        try:
            while True:
                if not self.runningTare:
                    oldValue = self.value
                    newValue = self.hx.get_weight(5)
                    if oldValue - newValue > -3000:
                        self.value = newValue
                        if self.value < 0:
                            self.value = 0

                    self.hx.reset()
                    time.sleep(0.5)
        except Exception as e:
            self.app.logger.info('Exception calculating WaterLevel value %s', self.name)
            self.app.logger.exception(e)