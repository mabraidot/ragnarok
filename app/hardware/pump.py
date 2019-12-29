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

        if self.getStatus() == waterActionsEnum.WATER_IN_FILTERED:
            if self.app.boilKettle.getWaterLevelSetPoint() > 0 and self.app.boilKettle.getWaterLevel() >= self.app.boilKettle.getWaterLevelSetPoint():
                self.app.boilKettleValveInlet.set(0)
                self.app.boilKettle.setWaterLevel(0)
                self.setStatus(waterActionsEnum.FINISHED)



    def moveWater(self, action = waterActionsEnum.FINISHED, ammount = 0, time = 0):
        if not isinstance(action, waterActionsEnum):
            raise TypeError("%s attribute must be set to an instance of %s" % (action, waterActionsEnum))

        self.setStatus(action)

        if action == waterActionsEnum.WATER_IN_FILTERED:
            if ammount > 0:
                self.app.boilKettle.setWaterLevel(ammount)
                self.app.boilKettleValveInlet.set(100)
            

