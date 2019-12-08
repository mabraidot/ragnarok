import random

class waterLevelProbe:
    def __init__(self, app, name = 'MashTunWaterLevelProbe'):
        self.app = app
        self.name = name
        self.value = 0
    
    def get(self):
        # test value
        self.value = random.randrange(0, 16)
        return self.value
