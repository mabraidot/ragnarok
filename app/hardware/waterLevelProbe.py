from RPi import GPIO
from app.lib.hx711 import HX711
import random
import threading
import time
import statistics

class waterLevelProbe:
    def __init__(self, app, config, name = 'MashTunWaterLevelProbe'):
        self.app = app
        self.name = name
        self.config = config
        self.value = 0

        if self.config.get('ENVIRONMENT') == 'production':
            # https://github.com/tatobari/hx711py/blob/master/example.py
            # https://tutorials-raspberrypi.com/digital-raspberry-pi-scale-weight-sensor-hx711/
            self.hx = HX711(self.config.getint('WATER_LEVEL_SENSOR_DT'), self.config.getint('WATER_LEVEL_SENSOR_SCK'))
            self.hx.set_reading_format("MSB", "MSB")
            self.hx.set_reference_unit(self.config.getfloat('WATER_LEVEL_SENSOR_REFERENCE_UNIT'))
            self.tare()
            
            task = threading.Thread(target=self.run)
            task.start()


    def tare(self):
        self.hx.reset()
        self.hx.tare()


    def get(self):
        if self.config.get('ENVIRONMENT') == 'development':
            # TODO: this is a TEST. Return the actual value
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

        return self.value / 1000


    def run(self):
        try:
            valueList = []
            while True:
                valueList.append(self.hx.get_weight(5))
                if len(valueList) > 5:
                    self.value = statistics.median(valueList)
                    if self.value < 0:
                        self.value = 0
                    valueList = []
                time.sleep(0.1)
                # oldValue = self.value
                # newValue = self.hx.get_weight(5)
                # if oldValue - newValue > -1000:
                #     self.value = newValue
                #     if self.value < 0:
                #         self.value = 0

                # self.hx.power_down()
                # self.hx.power_up()
                # time.sleep(0.2)
        except:
            GPIO.cleanup()