from RPi import GPIO
from app.lib.sourcesEnum import sourcesEnum, waterActionsEnum, valveActions
from app.hardware.valve import valve
import threading

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
        GPIO.output(self.pin, GPIO.HIGH)
        self.oldWaterLevelValue = 0
        self.waterLevelReadingCount = 0
        self.initValves()
        

    def initValves(self):
        if self.config.get('DEFAULT', 'ENVIRONMENT') == 'production':
            from adafruit_servokit import ServoKit
            from RPi import GPIO
            self.app.servoKit = ServoKit(channels=8)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.config.getint('GENERAL_PINS','SERVO_ENABLE'), GPIO.OUT)
            GPIO.setwarnings(False)
            GPIO.output(self.config.getint('GENERAL_PINS','SERVO_ENABLE'), GPIO.HIGH)
        
        self.app.outletValveDump = valve(self.app, self.config, 0, 'OutletValveDump')
        self.app.chillerValveWort = valve(self.app, self.config, 1, 'ChillerValveWort')
        self.app.chillerValveWater = valve(self.app, self.config, 2, 'ChillerValveWater')
        self.app.boilKettleValveOutlet = valve(self.app, self.config, 3, 'BoilKettleValveOutlet')
        self.app.boilKettleValveReturn = valve(self.app, self.config, 4, 'BoilKettleValveReturn')
        self.app.mashTunValveOutlet = valve(self.app, self.config, 5, 'MashTunValveOutlet')
        self.app.mashTunValveInlet = valve(self.app, self.config, 6, 'MashTunValveInlet')
        # Valve inlet and waterin channels are shared
        self.app.boilKettleValveInlet = valve(self.app, self.config, 7, 'BoilKettleValveInlet')
        self.app.boilKettleValveWater = valve(self.app, self.config, 7, 'BoilKettleValveWater')

    def get(self):
        return self.value


    def set(self, newState = 'false'):
        if newState == 'true':
            self.value = True
            GPIO.output(self.pin, GPIO.LOW)
        else:
            self.value = False
            GPIO.output(self.pin, GPIO.HIGH)


    def getStatus(self):
        return self.status


    def setStatus(self, newStatus):
        if not isinstance(newStatus, waterActionsEnum):
            raise TypeError("%s attribute must be set to an instance of %s" % (newStatus, waterActionsEnum))
        self.status = newStatus


    def shutAllDown(self):
        self.setStatus(waterActionsEnum.FINISHED)
        self.set('false')
        self.app.boilKettleValveInlet.set(0)
        self.app.chillerValveWater.set(0)
        self.app.boilKettleValveWater.set(0)
        self.app.outletValveDump.set(0)
        self.app.chillerValveWort.set(0)
        self.app.boilKettleValveOutlet.set(0)
        self.app.boilKettleValveReturn.set(0)
        self.app.mashTunValveOutlet.set(0)
        self.app.mashTunValveInlet.set(0)
        self.time = 0
        if self.app.jobs.get_job('timerDelayedPump') is not None:
            self.app.jobs.remove_job('timerDelayedPump')


    def setDelayedPumpState(self):
        self.set('true')
        self.app.jobs.remove_job('timerDelayedPump')


    def valvesRunWaterIn(self, state = valveActions.CLOSE):
        if state == valveActions.OPEN:
            self.app.boilKettleValveInlet.set(100)
        else:
            self.app.boilKettleValveInlet.set(0)

    def valvesRunMashTunToKettle(self, state = valveActions.CLOSE):
        if state == valveActions.OPEN:
            self.app.mashTunValveOutlet.set(100)
            self.app.boilKettleValveReturn.set(60)
        else:
            self.app.mashTunValveOutlet.set(0)
            self.app.boilKettleValveReturn.set(0)

    def valvesRunKettleToMashTun(self, state = valveActions.CLOSE):
        if state == valveActions.OPEN:
            self.app.boilKettleValveOutlet.set(100)
            self.app.mashTunValveInlet.set(60)
        else:
            self.app.boilKettleValveOutlet.set(0)
            self.app.mashTunValveInlet.set(0)

    def valvesRunMashTunToMashTun(self, state = valveActions.CLOSE):
        if state == valveActions.OPEN:
            self.app.mashTunValveOutlet.set(100)
            self.app.mashTunValveInlet.set(40)
        else:
            self.app.mashTunValveOutlet.set(0)
            self.app.mashTunValveInlet.set(0)

    def valvesRunKettleToKettle(self, state = valveActions.CLOSE):
        if state == valveActions.OPEN:
            self.app.boilKettleValveOutlet.set(100)
            self.app.boilKettleValveReturn.set(40)
        else:
            self.app.boilKettleValveOutlet.set(0)
            self.app.boilKettleValveReturn.set(0)

    def valvesRunChill(self, state = valveActions.CLOSE):
        if state == valveActions.OPEN:
            self.app.chillerValveWater.set(100)
            self.app.boilKettleValveOutlet.set(100)
            self.app.chillerValveWort.set(40)
        else:
            self.app.chillerValveWater.set(0)
            self.app.boilKettleValveOutlet.set(0)
            self.app.chillerValveWort.set(0)

    def pumpDaemon(self):

        # Fill in the kettle with filtered or non-filtered tap water
        if self.getStatus() == waterActionsEnum.WATER_IN_FILTERED or self.getStatus() == waterActionsEnum.WATER_IN:
            if (self.app.boilKettle.getWaterLevelSetPoint() > 0 and 
                (self.app.boilKettle.getWaterLevel() >= self.app.boilKettle.getWaterLevelSetPoint() or 
                self.app.boilKettle.getWaterLevel() >= self.config.getfloat('DEFAULT', 'MAX_WATER_LEVEL'))):

                # self.app.boilKettleValveInlet.set(0)
                task = threading.Thread(target=self.valvesRunWaterIn, kwargs=dict(state=valveActions.CLOSE))
                task.start()
                self.app.boilKettle.setWaterLevel(0)
                self.setStatus(waterActionsEnum.FINISHED)

        # Rack water from boilkettle to mashtun
        if self.getStatus() == waterActionsEnum.KETTLE_TO_MASHTUN:
            if self.get() and abs(self.oldWaterLevelValue - self.app.boilKettle.getWaterLevel()) < 0.1:
                self.waterLevelReadingCount += 1
            self.oldWaterLevelValue = self.app.boilKettle.getWaterLevel()

            if (self.waterLevelReadingCount >= 3 or 
                self.app.boilKettle.getWaterLevel() <= 0 or 
                self.app.mashTun.getWaterLevel() >= self.app.mashTun.getWaterLevelSetPoint() or
                self.app.mashTun.getWaterLevel() >= self.config.getfloat('DEFAULT', 'MAX_WATER_LEVEL')):

                self.set('false')
                # self.app.boilKettleValveOutlet.set(0)
                # self.app.mashTunValveInlet.set(0)
                task = threading.Thread(target=self.valvesRunKettleToMashTun, kwargs=dict(state=valveActions.CLOSE))
                task.start()
                self.setStatus(waterActionsEnum.FINISHED)
                self.oldWaterLevelValue = 0
                self.waterLevelReadingCount = 0

        # Rack water from mashtun to boilkettle
        if self.getStatus() == waterActionsEnum.MASHTUN_TO_KETTLE:
            if self.get() and abs(self.oldWaterLevelValue - self.app.mashTun.getWaterLevel()) < 0.1:
                self.waterLevelReadingCount += 1
            self.oldWaterLevelValue = self.app.mashTun.getWaterLevel()

            if (self.waterLevelReadingCount >= 3 or 
                self.app.mashTun.getWaterLevel() <= 0 or 
                self.app.boilKettle.getWaterLevel() >= self.app.boilKettle.getWaterLevelSetPoint() or 
                self.app.boilKettle.getWaterLevel() >= self.config.getfloat('DEFAULT', 'MAX_WATER_LEVEL')):

                self.set('false')
                # self.app.mashTunValveOutlet.set(0)
                # self.app.boilKettleValveReturn.set(0)
                task = threading.Thread(target=self.valvesRunMashTunToKettle, kwargs=dict(state=valveActions.CLOSE))
                task.start()
                self.setStatus(waterActionsEnum.FINISHED)
                self.oldWaterLevelValue = 0
                self.waterLevelReadingCount = 0

        # Recirculation through mashtun
        if self.getStatus() == waterActionsEnum.MASHTUN_TO_MASHTUN:
            if self.time <= 0:
                self.time = 0
                self.set('false')
                # self.app.mashTunValveOutlet.set(0)
                # self.app.mashTunValveInlet.set(0)
                task = threading.Thread(target=self.valvesRunMashTunToMashTun, kwargs=dict(state=valveActions.CLOSE))
                task.start()
                self.setStatus(waterActionsEnum.FINISHED)
            else:
                self.time -= 1

        # Recirculation through boil kettle
        if self.getStatus() == waterActionsEnum.KETTLE_TO_KETTLE:
            if self.time <= 0:
                self.time = 0
                self.set('false')
                # self.app.boilKettleValveOutlet.set(0)
                # self.app.boilKettleValveReturn.set(0)
                task = threading.Thread(target=self.valvesRunKettleToKettle, kwargs=dict(state=valveActions.CLOSE))
                task.start()
                self.setStatus(waterActionsEnum.FINISHED)
            else:
                self.time -= 1





    def moveWater(self, action = waterActionsEnum.FINISHED, ammount = 0, time = 0):
        if not isinstance(action, waterActionsEnum):
            raise TypeError("%s attribute must be set to an instance of %s" % (action, waterActionsEnum))
        
        if ((self.getStatus() == waterActionsEnum.KETTLE_TO_KETTLE or self.getStatus() == waterActionsEnum.MASHTUN_TO_MASHTUN) 
            and action != waterActionsEnum.FINISHED):
            task = threading.Thread(target=self.shutAllDown)
            task.start()
            # self.shutAllDown()

        if time > 0:
            self.time = int(time)

        if self.getStatus() == waterActionsEnum.FINISHED:
            self.setStatus(action)

            # Fill in the kettle with filtered or non-filtered tap water
            if action == waterActionsEnum.WATER_IN_FILTERED or action == waterActionsEnum.WATER_IN:
                if ammount > 0:
                    self.app.boilKettle.setWaterLevel(max(ammount, self.config.getfloat('DEFAULT', 'SAFE_WATER_LEVEL_FOR_HEATERS')))
                    if self.app.boilKettle.getWaterLevel() < self.app.boilKettle.getWaterLevelSetPoint():
                        # self.app.boilKettleValveInlet.set(100)
                        task = threading.Thread(target=self.valvesRunWaterIn, kwargs=dict(state=valveActions.OPEN))
                        task.start()

            # Rack water from boilkettle to mashtun
            if action == waterActionsEnum.KETTLE_TO_MASHTUN:
                self.app.mashTun.setWaterLevel(self.app.mashTun.getWaterLevel() + self.app.boilKettle.getWaterLevel())
                # self.app.boilKettleValveOutlet.set(100)
                # self.app.mashTunValveInlet.set(60)
                task = threading.Thread(target=self.valvesRunKettleToMashTun, kwargs=dict(state=valveActions.OPEN))
                task.start()
                self.app.jobs.add_job(
                    self.setDelayedPumpState, 
                    'interval', 
                    seconds=self.config.getint('DEFAULT', 'PUMP_PRIMING_TIME'), 
                    id='timerDelayedPump',
                    replace_existing=True)

            # Rack water from mashtun to boilkettle
            if action == waterActionsEnum.MASHTUN_TO_KETTLE:
                self.app.boilKettle.setWaterLevel(self.app.boilKettle.getWaterLevel() + self.app.mashTun.getWaterLevel())
                # self.app.mashTunValveOutlet.set(100)
                # self.app.boilKettleValveReturn.set(60)
                task = threading.Thread(target=self.valvesRunMashTunToKettle, kwargs=dict(state=valveActions.OPEN))
                task.start()
                self.app.jobs.add_job(
                    self.setDelayedPumpState, 
                    'interval', 
                    seconds=self.config.getint('DEFAULT', 'PUMP_PRIMING_TIME'), 
                    id='timerDelayedPump',
                    replace_existing=True)

            # Recirculation through boil kettle
            if action == waterActionsEnum.KETTLE_TO_KETTLE:
                # self.app.boilKettleValveOutlet.set(100)
                # self.app.boilKettleValveReturn.set(40)
                task = threading.Thread(target=self.valvesRunKettleToKettle, kwargs=dict(state=valveActions.OPEN))
                task.start()
                self.app.jobs.add_job(
                    self.setDelayedPumpState, 
                    'interval', 
                    seconds=self.config.getint('DEFAULT', 'PUMP_PRIMING_TIME'), 
                    id='timerDelayedPump',
                    replace_existing=True)

            # Recirculation through CHILLmashtun
            if action == waterActionsEnum.MASHTUN_TO_MASHTUN:
                # self.app.mashTunValveOutlet.set(100)
                # self.app.mashTunValveInlet.set(40)
                task = threading.Thread(target=self.valvesRunMashTunToMashTun, kwargs=dict(state=valveActions.OPEN))
                task.start()
                self.app.jobs.add_job(
                    self.setDelayedPumpState, 
                    'interval', 
                    seconds=self.config.getint('DEFAULT', 'PUMP_PRIMING_TIME'), 
                    id='timerDelayedPump',
                    replace_existing=True)

            # Recirculation through chiller to cool the wort
            if action == waterActionsEnum.CHILL:
                # self.app.chillerValveWater.set(100)
                # self.app.boilKettleValveOutlet.set(100)
                # self.app.chillerValveWort.set(40)
                task = threading.Thread(target=self.valvesRunChill, kwargs=dict(state=valveActions.OPEN))
                task.start()
                self.app.jobs.add_job(
                    self.setDelayedPumpState, 
                    'interval', 
                    seconds=self.config.getint('DEFAULT', 'PUMP_PRIMING_TIME'), 
                    id='timerDelayedPump',
                    replace_existing=True)

        if action == waterActionsEnum.FINISHED:
            task = threading.Thread(target=self.shutAllDown)
            task.start()
            # self.shutAllDown()
