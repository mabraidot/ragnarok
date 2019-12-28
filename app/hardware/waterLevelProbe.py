import random

class waterLevelProbe:
    def __init__(self, app, config, name = 'MashTunWaterLevelProbe'):
        self.app = app
        self.name = name
        self.config = config
        self.value = 0
    
    def get(self):
        # TODO: this is a TEST. Return the actual value
        flow = 0.5
        if self.name == 'MashTunWaterLevelProbe':
            if self.app.pump.get():
                inletValveState = self.app.mashTunValveInlet.get()
                outletValveState = self.app.mashTunValveOutlet.get()
                if inletValveState > 0:
                    self.value += flow
                elif outletValveState > 0:
                    self.value -= flow

        else:
            if self.app.pump.get():
                inletValveState = self.app.boilKettleValveInlet.get()
                waterValveState = self.app.boilKettleValveWater.get()
                returnValveState = self.app.boilKettleValveReturn.get()
                outletValveState = self.app.boilKettleValveOutlet.get()

                if inletValveState > 0 or waterValveState > 0 or returnValveState > 0:
                    self.value += flow
                elif outletValveState > 0:
                    self.value -= flow * (outletValveState / 100)

        return self.value
