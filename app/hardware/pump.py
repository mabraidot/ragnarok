from app.hardware.sourcesEnum import sourcesEnum

class pump:
    def __init__(self, app, name):
        self.app = app
        self.name = name
        self.value = False
    
    def get(self):
        return self.value
    
    def set(self, newState = 'false'):
        if newState == 'true':
            self.value = True
        else:
            self.value = False
            self.close()

    def close(self):
        self.app.outletValveDump.set(0)
        self.app.chillerValveWort.set(0)
        self.app.chillerValveWater.set(0)
        self.app.boilKettleValveOutlet.set(0)
        self.app.boilKettleValveInlet.set(0)
        self.app.boilKettleValveWater.set(0)
        self.app.boilKettleValveReturn.set(0)
        self.app.mashTunValveOutlet.set(0)
        self.app.mashTunValveInlet.set(0)


    def moveWater(self, moveFrom, moveTo = None, speed = 100):
        if not isinstance(speed, int) or speed < 0 or speed > 100:
            raise TypeError("%s attribute must be set to an instance of %s and in a range of (0-100)" % (speed, int))
        if not isinstance(moveFrom, sourcesEnum):
            raise TypeError("%s attribute must be set to an instance of %s" % (moveFrom, sourcesEnum))
        if moveTo != None and not isinstance(moveTo, sourcesEnum):
            raise TypeError("%s attribute must be set to an instance of %s" % (moveTo, sourcesEnum))

        if moveFrom == sourcesEnum.BOILKETTLE_INLET:
            self.app.boilKettleValveInlet.set(speed)

        self.set('true')
