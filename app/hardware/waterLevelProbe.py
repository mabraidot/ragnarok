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

        if self.config.get('ENVIRONMENT') == 'production':
            # https://github.com/tatobari/hx711py/blob/master/example.py
            # https://tutorials-raspberrypi.com/digital-raspberry-pi-scale-weight-sensor-hx711/
            self.hx = HX711(self.config.getint('WATER_LEVEL_SENSOR_DT'), self.config.getint('WATER_LEVEL_SENSOR_SCK'))
            self.hx.set_reading_format("MSB", "MSB")
            self.hx.set_reference_unit(self.config.getint('WATER_LEVEL_SENSOR_REFERENCE_UNIT'))
            self.hx.reset()
            self.hx.tare()
            
            task = threading.Thread(target=self.run)
            task.start()


    def get(self):
        if self.config.get('ENVIRONMENT') == 'development':
            # TODO: this is a TEST. Return the actual value
            flow = 0.2
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

        return self.value


    def run(self):
        try:
            while True:
                self.value = self.hx.get_weight(5)
                self.hx.power_down()
                self.hx.power_up()
                time.sleep(0.2)
        except:
            GPIO.cleanup()