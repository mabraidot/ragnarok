import random

class waterLevelProbe:
    def __init__(self, app, config, name = 'MashTunWaterLevelProbe'):
        self.app = app
        self.name = name
        self.config = config
        self.value = 0
    
    def get(self):
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
