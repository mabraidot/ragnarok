import random

class temperatureProbe:
    def __init__(self, app, name = 'MashTunTemperatureProbe'):
        self.app = app
        self.name = name
        self.value = 0

        # https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/
        # https://learn.adafruit.com/adafruit-max31865-rtd-pt100-amplifier/python-circuitpython


    def get(self):
        # TODO: this is a TEST. Return the actual value
        heater = self.app.mashTun.getHeater()
        pwm = self.app.mashTun.getPWM()
        if self.name == 'BoilKettleTemperatureProbe':
            heater = self.app.boilKettle.getHeater()
            pwm = self.app.boilKettle.getPWM()
        if heater and pwm > 0 and self.value < 110:
            self.value += 1 * (pwm / 100)
        elif self.value > 0:
            self.value -= 0.1

        return self.value
