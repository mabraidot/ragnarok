from app.hardware.sourcesEnum import sourcesEnum, waterActionsEnum

class pump:
    def __init__(self, app, name):
        self.app = app
        self.name = name
        self.value = False
        self.app.jobs.add_job(self.pumpDaemon, 'interval', seconds=1, id='pumpDaemon')
        self.status = waterActionsEnum.FINISHED
    
    def get(self):
        return self.value
    
    def set(self, newState = 'false'):
        if newState == 'true':
            self.value = True
        else:
            self.value = False

    def getStatus(self):
        return self.status
    
    def setStatus(self, newStatus):
        if not isinstance(newStatus, waterActionsEnum):
            raise TypeError("%s attribute must be set to an instance of %s" % (newStatus, waterActionsEnum))
        self.status = newStatus


    def pumpDaemon(self):

        # Fill in the kettle with filtered or non-filtered tap water
        if self.getStatus() == waterActionsEnum.WATER_IN_FILTERED or self.getStatus() == waterActionsEnum.WATER_IN:
            if (self.app.boilKettle.getWaterLevelSetPoint() > 0 and 
                self.app.boilKettle.getWaterLevel() >= self.app.boilKettle.getWaterLevelSetPoint()):

                self.app.boilKettleValveInlet.set(0)
                self.app.boilKettle.setWaterLevel(0)
                self.setStatus(waterActionsEnum.FINISHED)

        # Rack water from boilkettle to mashtun
        if self.getStatus() == waterActionsEnum.KETTLE_TO_MASHTUN:
            if (self.app.boilKettle.getWaterLevel() <= 0 or 
                self.app.mashTun.getWaterLevel() == self.app.mashTun.getWaterLevelSetPoint()):

                self.set('true')
                self.app.boilKettleValveOutlet.set(0)
                self.app.mashTunValveInlet.set(0)





    def moveWater(self, action = waterActionsEnum.FINISHED, ammount = 0, time = 0):
        if not isinstance(action, waterActionsEnum):
            raise TypeError("%s attribute must be set to an instance of %s" % (action, waterActionsEnum))

        self.setStatus(action)

        # Fill in the kettle with filtered or non-filtered tap water
        if action == waterActionsEnum.WATER_IN_FILTERED or action == waterActionsEnum.WATER_IN:
            if ammount > 0:
                self.app.boilKettle.setWaterLevel(ammount)
                self.app.boilKettleValveInlet.set(100)

        # Rack water from boilkettle to mashtun
        if action == waterActionsEnum.KETTLE_TO_MASHTUN:
            self.app.mashTun.setWaterLevel(self.app.boilKettle.getWaterLevel())
            self.app.boilKettleValveOutlet.set(100)
            self.app.mashTunValveInlet.set(100)
            self.set('true')


