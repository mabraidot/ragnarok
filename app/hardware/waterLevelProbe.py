import random

class waterLevelProbe:
    def __init__(self, app, name = 'MashTunWaterLevelProbe'):
        self.app = app
        self.name = name
        self.value = 0
    
    def get(self):
        # TODO: this is a TEST. Return the actual value
        # self.value = random.randrange(0, 16)
        if self.app.pump.get() and self.value < 15:
            self.value += 0.3

        return self.value
