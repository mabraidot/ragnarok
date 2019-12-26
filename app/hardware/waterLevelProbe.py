import random

class waterLevelProbe:
    def __init__(self, app, config, name = 'MashTunWaterLevelProbe'):
        self.app = app
        self.name = name
        self.config = config
        self.value = 0
    
    def get(self):
        # TODO: this is a TEST. Return the actual value
        if self.name == 'MashTunWaterLevelProbe':
            currentSetPoint = self.app.mashTun.getWaterLevelSetPoint()
        else:
            currentSetPoint = self.app.boilKettle.getWaterLevelSetPoint()

        if self.app.pump.get() and currentSetPoint > 0:
            self.value += 0.3

        return self.value
