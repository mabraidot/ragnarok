import random

class temperatureProbe:
    def __init__(self, app, name = 'MashTunTemperatureProbe'):
        self.app = app
        self.name = name
        self.value = 0
    
    def get(self):
        # @TODO: this is a TEST. Return the actual value
        heater = self.app.mashTun.getHeater()
        if self.name == 'BoilKettleTemperatureProbe':
            heater = self.app.boilKettle.getHeater()
        if heater and self.value < 110:
            self.value += 1
        elif self.value > 0:
            self.value -= 0.1

        return self.value
