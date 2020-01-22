from RPi import GPIO
from app.hardware.sourcesEnum import sourcesEnum, waterActionsEnum

class pump:
    def __init__(self, app, config, name):
        self.app = app
        self.config = config
        self.name = name
        self.value = False
        self.time = 0
        self.app.jobs.add_job(self.pumpDaemon, 'interval', seconds=1, id='pumpDaemon')
        self.status = waterActionsEnum.FINISHED
        self.pin = self.config.getint('GENERAL_PINS', 'PUMP')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.setwarnings(False)


    def get(self):
        return self.value


    def set(self, newState = 'false'):
        if newState == 'true':
            self.value = True
            GPIO.output(self.pin, GPIO.HIGH)
        else:
            self.value = False
            GPIO.output(self.pin, GPIO.LOW)


    def getStatus(self):
        return self.status


    def setStatus(self, newStatus):
        if not isinstance(newStatus, waterActionsEnum):
            raise TypeError("%s attribute must be set to an instance of %s" % (newStatus, waterActionsEnum))
        self.status = newStatus


    def shutAllDown(self):
        self.setStatus(waterActionsEnum.FINISHED)
        self.set('false')
        self.app.outletValveDump.set(0)
        self.app.chillerValveWort.set(0)
        self.app.chillerValveWater.set(0)
        self.app.boilKettleValveOutlet.set(0)
        self.app.boilKettleValveInlet.set(0)
        self.app.boilKettleValveWater.set(0)
        self.app.boilKettleValveReturn.set(0)
        self.app.mashTunValveOutlet.set(0)
        self.app.mashTunValveInlet.set(0)
        self.time = 0
        if self.app.jobs.get_job('timerDelayedPump') is not None:
            self.app.jobs.remove_job('timerDelayedPump')


    def setDelayedPumpState(self):
        self.set('true')
        self.app.jobs.remove_job('timerDelayedPump')


    def pumpDaemon(self):

        # Fill in the kettle with filtered or non-filtered tap water
        if self.getStatus() == waterActionsEnum.WATER_IN_FILTERED or self.getStatus() == waterActionsEnum.WATER_IN:
            if (self.app.boilKettle.getWaterLevelSetPoint() > 0 and 
                (self.app.boilKettle.getWaterLevel() >= self.app.boilKettle.getWaterLevelSetPoint() or 
                self.app.boilKettle.getWaterLevel() >= self.config.getfloat('DEFAULT', 'MAX_WATER_LEVEL'))):

                self.app.boilKettleValveInlet.set(0)
                self.app.boilKettle.setWaterLevel(0)
                self.setStatus(waterActionsEnum.FINISHED)

        # Rack water from boilkettle to mashtun
        if self.getStatus() == waterActionsEnum.KETTLE_TO_MASHTUN:
            if (self.app.boilKettle.getWaterLevel() <= 0 or 
                self.app.mashTun.getWaterLevel() >= self.app.mashTun.getWaterLevelSetPoint() or
                self.app.mashTun.getWaterLevel() >= self.config.getfloat('DEFAULT', 'MAX_WATER_LEVEL')):

                self.set('false')
                self.app.boilKettleValveOutlet.set(0)
                self.app.mashTunValveInlet.set(0)
                self.setStatus(waterActionsEnum.FINISHED)

        # Rack water from mashtun to boilkettle
        if self.getStatus() == waterActionsEnum.MASHTUN_TO_KETTLE:
            if (self.app.mashTun.getWaterLevel() <= 0 or 
                self.app.boilKettle.getWaterLevel() >= self.app.boilKettle.getWaterLevelSetPoint() or 
                self.app.boilKettle.getWaterLevel() >= self.config.getfloat('DEFAULT', 'MAX_WATER_LEVEL')):

                self.set('false')
                self.app.mashTunValveOutlet.set(0)
                self.app.boilKettleValveReturn.set(0)
                self.setStatus(waterActionsEnum.FINISHED)

        # Recirculation through mashtun
        if self.getStatus() == waterActionsEnum.MASHTUN_TO_MASHTUN:
            if self.time <= 0:
                self.time = 0
                self.set('false')
                self.app.mashTunValveOutlet.set(0)
                self.app.mashTunValveInlet.set(0)
            else:
                self.time -= 1

        # Recirculation through boil kettle
        if self.getStatus() == waterActionsEnum.KETTLE_TO_KETTLE:
            if self.time <= 0:
                self.time = 0
                self.set('false')
                self.app.boilKettleValveOutlet.set(0)
                self.app.boilKettleValveReturn.set(0)
            else:
                self.time -= 1





    def moveWater(self, action = waterActionsEnum.FINISHED, ammount = 0, time = 0):
        if not isinstance(action, waterActionsEnum):
            raise TypeError("%s attribute must be set to an instance of %s" % (action, waterActionsEnum))
        
        if ((self.getStatus() == waterActionsEnum.KETTLE_TO_KETTLE or self.getStatus() == waterActionsEnum.MASHTUN_TO_MASHTUN) 
            and action != waterActionsEnum.FINISHED):
            self.shutAllDown()

        if time > 0:
            self.time = int(time)

        if self.getStatus() == waterActionsEnum.FINISHED:
            self.setStatus(action)

            # Fill in the kettle with filtered or non-filtered tap water
            if action == waterActionsEnum.WATER_IN_FILTERED or action == waterActionsEnum.WATER_IN:
                if ammount > 0:
                    self.app.boilKettle.setWaterLevel(max(ammount, self.config.getfloat('DEFAULT', 'SAFE_WATER_LEVEL_FOR_HEATERS')))
                    if self.app.boilKettle.getWaterLevel() < self.app.boilKettle.getWaterLevelSetPoint():
                        self.app.boilKettleValveInlet.set(100)

            # Rack water from boilkettle to mashtun
            if action == waterActionsEnum.KETTLE_TO_MASHTUN:
                self.app.mashTun.setWaterLevel(self.app.mashTun.getWaterLevel() + self.app.boilKettle.getWaterLevel())
                self.app.boilKettleValveOutlet.set(100)
                self.app.mashTunValveInlet.set(100)
                self.app.jobs.add_job(
                    self.setDelayedPumpState, 
                    'interval', 
                    seconds=self.config.getint('DEFAULT', 'PUMP_PRIMING_TIME'), 
                    id='timerDelayedPump',
                    replace_existing=True,
                    max_instances=1)

            # Rack water from mashtun to boilkettle
            if action == waterActionsEnum.MASHTUN_TO_KETTLE:
                self.app.boilKettle.setWaterLevel(self.app.boilKettle.getWaterLevel() + self.app.mashTun.getWaterLevel())
                self.app.mashTunValveOutlet.set(100)
                self.app.boilKettleValveReturn.set(100)
                self.app.jobs.add_job(
                    self.setDelayedPumpState, 
                    'interval', 
                    seconds=self.config.getint('DEFAULT', 'PUMP_PRIMING_TIME'), 
                    id='timerDelayedPump',
                    replace_existing=True,
                    max_instances=1)

            # Recirculation through boil kettle
            if action == waterActionsEnum.KETTLE_TO_KETTLE:
                self.app.boilKettleValveOutlet.set(100)
                self.app.boilKettleValveReturn.set(40)
                self.app.jobs.add_job(
                    self.setDelayedPumpState, 
                    'interval', 
                    seconds=self.config.getint('DEFAULT', 'PUMP_PRIMING_TIME'), 
                    id='timerDelayedPump',
                    replace_existing=True,
                    max_instances=1)

            # Recirculation through mashtun
            if action == waterActionsEnum.MASHTUN_TO_MASHTUN:
                self.app.mashTunValveOutlet.set(100)
                self.app.mashTunValveInlet.set(40)
                self.app.jobs.add_job(
                    self.setDelayedPumpState, 
                    'interval', 
                    seconds=self.config.getint('DEFAULT', 'PUMP_PRIMING_TIME'), 
                    id='timerDelayedPump',
                    replace_existing=True,
                    max_instances=1)

            # Recirculation through chiller to cool the wort
            if action == waterActionsEnum.CHILL:
                self.app.chillerValveWater.set(100)
                self.app.boilKettleValveOutlet.set(100)
                self.app.chillerValveWort.set(40)
                self.app.jobs.add_job(
                    self.setDelayedPumpState, 
                    'interval', 
                    seconds=self.config.getint('DEFAULT', 'PUMP_PRIMING_TIME'), 
                    id='timerDelayedPump',
                    replace_existing=True,
                    max_instances=1)

        if action == waterActionsEnum.FINISHED:
            self.shutAllDown()
