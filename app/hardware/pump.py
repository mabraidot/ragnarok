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
        self.daemonTime = 0.5
        self.daemonRunningTime = 0.0
        self.app.jobs.add_job(self.pumpDaemon, 'interval', seconds=self.daemonTime, id='pumpDaemon')
        self.status = waterActionsEnum.FINISHED
        self.pin = self.config.getint('GENERAL_PINS', 'PUMP')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.setwarnings(False)
        GPIO.output(self.pin, GPIO.HIGH)
        self.oldMashTunWaterLevelValue = 0
        self.oldBoilKettleWaterLevelValue = 0
        self.originalMashTunWaterLevelValue = 0
        self.originalBoilKettleWaterLevelValue = 0
        self.amountToMove = 0
        self.waterLevelReadingCount = 0
        self.initValves()
        self.paused = False

        self.mashTunRecirculation = False
        self.boilKettleRecirculation = False
        self.recirculationMashTunFrequencyTime = self.config.getint('DEFAULT', 'RECIRCULATION_MASHTUN_FREQUENCY_TIME')
        self.recirculationBoilKettleFrequencyTime = self.config.getint('DEFAULT', 'RECIRCULATION_BOILKETTLE_FREQUENCY_TIME')
        self.recirculationMashTunTime = self.config.getint('DEFAULT', 'RECIRCULATION_MASHTUN_TIME')
        self.recirculationBoilKettleTime = self.config.getint('DEFAULT', 'RECIRCULATION_BOILKETTLE_TIME')
        self.recirculationStatus = valveActions.CLOSE


    def setMashTunRecirculation(self, status):
        if status:
            self.mashTunRecirculation = True
        else:
            self.mashTunRecirculation = False

    def setBoilKettleRecirculation(self, status):
        if status:
            self.boilKettleRecirculation = True
        else:
            self.boilKettleRecirculation = False


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
            self.daemonRunningTime = 0
            GPIO.output(self.pin, GPIO.HIGH)


    def getStatus(self):
        return self.status


    def setStatus(self, newStatus):
        if not isinstance(newStatus, waterActionsEnum):
            raise TypeError("%s attribute must be set to an instance of %s" % (newStatus, waterActionsEnum))
        self.status = newStatus
        self.app.logger.info('[PUMP] Set new status: %s', newStatus)


    def openAllVaves(self):
        self.app.boilKettleValveInlet.set(100)
        self.app.chillerValveWater.set(100)
        # self.app.boilKettleValveWater.set(100)
        self.app.outletValveDump.set(100)
        self.app.chillerValveWort.set(100)
        self.app.boilKettleValveOutlet.set(100)
        self.app.boilKettleValveReturn.set(100)
        self.app.mashTunValveOutlet.set(100)
        self.app.mashTunValveInlet.set(100)


    def shutAllDown(self):
        self.app.logger.info('[PUMP] Shutting all down')
        self.setStatus(waterActionsEnum.BUSY)
        self.set('false')
        self.app.boilKettleValveInlet.set(0)
        self.app.chillerValveWater.set(0)
        # self.app.boilKettleValveWater.set(0)
        self.app.outletValveDump.set(0)
        self.app.chillerValveWort.set(0)
        self.app.boilKettleValveOutlet.set(0)
        self.app.boilKettleValveReturn.set(0)
        self.app.mashTunValveOutlet.set(0)
        self.app.mashTunValveInlet.set(0)
        self.setStatus(waterActionsEnum.FINISHED)
        self.time = 0
        if self.app.jobs.get_job('timerDelayedPump') is not None:
            self.app.jobs.remove_job('timerDelayedPump')
        self.app.logger.info('[PUMP] Shutted all down')


    def setDelayedPumpState(self):
        self.set('true')
        if self.app.jobs.get_job('timerDelayedPump') is not None:
            self.app.jobs.remove_job('timerDelayedPump')


    def valvesRunWaterIn(self, state = valveActions.CLOSE):
        if state == valveActions.OPEN:
            currentAction = self.getStatus()
            self.setStatus(waterActionsEnum.BUSY)
            if self.mashTunRecirculation:
                self.valvesRunMashTunToMashTun(state=valveActions.CLOSE, silent=True)
            if self.boilKettleRecirculation:
                self.valvesRunKettleToKettle(state=valveActions.CLOSE, silent=True)
            self.app.boilKettleValveInlet.set(60)
            self.setStatus(currentAction)
        else:
            self.app.boilKettleValveInlet.set(0)
            self.setStatus(waterActionsEnum.FINISHED)

    def valvesRunMashTunToKettle(self, state = valveActions.CLOSE):
        if state == valveActions.OPEN:
            currentAction = self.getStatus()
            self.setStatus(waterActionsEnum.BUSY)
            if self.mashTunRecirculation:
                self.valvesRunMashTunToMashTun(state=valveActions.CLOSE, silent=True)
            if self.boilKettleRecirculation:
                self.valvesRunKettleToKettle(state=valveActions.CLOSE, silent=True)
            if self.app.cleaning.isRunning():
                self.app.boilKettleValveReturn.set(100)
            else:
                self.app.boilKettleValveReturn.set(70)
            self.app.mashTunValveOutlet.set(100)
            self.app.jobs.add_job(
                self.setDelayedPumpState, 
                'interval', 
                seconds=self.config.getint('DEFAULT', 'PUMP_PRIMING_TIME'), 
                id='timerDelayedPump',
                replace_existing=True)
            self.setStatus(currentAction)
        else:
            self.set('false')
            if self.app.jobs.get_job('timerDelayedPump') is not None:
                self.app.jobs.remove_job('timerDelayedPump')
            self.app.boilKettleValveReturn.set(0)
            self.app.mashTunValveOutlet.set(0)
            self.setStatus(waterActionsEnum.FINISHED)

    def valvesRunKettleToMashTun(self, state = valveActions.CLOSE):
        if state == valveActions.OPEN:
            currentAction = self.getStatus()
            self.setStatus(waterActionsEnum.BUSY)
            if self.mashTunRecirculation:
                self.valvesRunMashTunToMashTun(state=valveActions.CLOSE, silent=True)
            if self.boilKettleRecirculation:
                self.valvesRunKettleToKettle(state=valveActions.CLOSE, silent=True)
            if self.app.cleaning.isRunning():
                self.app.mashTunValveInlet.set(100)
            else:
                self.app.mashTunValveInlet.set(70)
            self.app.boilKettleValveOutlet.set(100)
            self.app.jobs.add_job(
                self.setDelayedPumpState, 
                'interval', 
                seconds=self.config.getint('DEFAULT', 'PUMP_PRIMING_TIME'), 
                id='timerDelayedPump',
                replace_existing=True)
            self.setStatus(currentAction)
        else:
            self.set('false')
            if self.app.jobs.get_job('timerDelayedPump') is not None:
                self.app.jobs.remove_job('timerDelayedPump')
            self.app.mashTunValveInlet.set(0)
            self.app.boilKettleValveOutlet.set(0)
            self.setStatus(waterActionsEnum.FINISHED)

    def valvesRunMashTunToMashTun(self, state = valveActions.CLOSE, silent = False):
        if state == valveActions.OPEN:
            currentAction = self.getStatus()
            self.setStatus(waterActionsEnum.BUSY)
            if self.boilKettleRecirculation:
                self.valvesRunKettleToKettle(state=valveActions.CLOSE, silent=True)
            if silent:
                self.recirculationStatus = valveActions.OPEN
            if self.app.cleaning.isRunning():
                self.app.mashTunValveInlet.set(100)
            else:
                self.app.mashTunValveInlet.set(70)
            self.app.mashTunValveOutlet.set(100)
            self.app.jobs.add_job(
                self.setDelayedPumpState, 
                'interval', 
                seconds=self.config.getint('DEFAULT', 'PUMP_PRIMING_TIME'), 
                id='timerDelayedPump',
                replace_existing=True)
            self.setStatus(currentAction)
        else:
            if silent:
                self.recirculationStatus = valveActions.CLOSE
            self.set('false')
            if self.app.jobs.get_job('timerDelayedPump') is not None:
                self.app.jobs.remove_job('timerDelayedPump')
            self.app.mashTunValveInlet.set(0)
            self.app.mashTunValveOutlet.set(0)
            if not silent:
                self.setStatus(waterActionsEnum.FINISHED)

    def valvesRunKettleToKettle(self, state = valveActions.CLOSE, silent = False):
        if state == valveActions.OPEN:
            currentAction = self.getStatus()
            self.setStatus(waterActionsEnum.BUSY)
            if self.mashTunRecirculation:
                self.valvesRunMashTunToMashTun(state=valveActions.CLOSE, silent=True)
            if silent:
                self.recirculationStatus = valveActions.OPEN
            if self.app.cleaning.isRunning():
                self.app.boilKettleValveReturn.set(100)
            else:
                self.app.boilKettleValveReturn.set(70)
            self.app.boilKettleValveOutlet.set(100)
            self.app.jobs.add_job(
                self.setDelayedPumpState, 
                'interval', 
                seconds=self.config.getint('DEFAULT', 'PUMP_PRIMING_TIME'), 
                id='timerDelayedPump',
                replace_existing=True)
            self.setStatus(currentAction)
        else:
            if silent:
                self.recirculationStatus = valveActions.CLOSE
            self.set('false')
            if self.app.jobs.get_job('timerDelayedPump') is not None:
                self.app.jobs.remove_job('timerDelayedPump')
            self.app.boilKettleValveReturn.set(0)
            self.app.boilKettleValveOutlet.set(0)
            if not silent:
                self.setStatus(waterActionsEnum.FINISHED)

    def valvesRunKettleToChiller(self, state = valveActions.CLOSE):
        if state == valveActions.OPEN:
            currentAction = self.getStatus()
            self.setStatus(waterActionsEnum.BUSY)
            if self.mashTunRecirculation:
                self.valvesRunMashTunToMashTun(state=valveActions.CLOSE, silent=True)
            if self.boilKettleRecirculation:
                self.valvesRunKettleToKettle(state=valveActions.CLOSE, silent=True)
            self.app.chillerValveWort.set(100)
            self.app.boilKettleValveOutlet.set(100)
            self.app.jobs.add_job(
                self.setDelayedPumpState, 
                'interval', 
                seconds=self.config.getint('DEFAULT', 'PUMP_PRIMING_TIME'), 
                id='timerDelayedPump',
                replace_existing=True)
            self.setStatus(currentAction)
        else:
            self.set('false')
            if self.app.jobs.get_job('timerDelayedPump') is not None:
                self.app.jobs.remove_job('timerDelayedPump')
            self.app.chillerValveWort.set(0)
            self.app.boilKettleValveOutlet.set(0)
            self.setStatus(waterActionsEnum.FINISHED)

    def valvesRunChill(self, state = valveActions.CLOSE):
        if state == valveActions.OPEN:
            currentAction = self.getStatus()
            self.setStatus(waterActionsEnum.BUSY)
            if self.mashTunRecirculation:
                self.valvesRunMashTunToMashTun(state=valveActions.CLOSE, silent=True)
            if self.boilKettleRecirculation:
                self.valvesRunKettleToKettle(state=valveActions.CLOSE, silent=True)
            self.app.boilKettleValveOutlet.set(100)
            self.app.chillerValveWort.set(35)
            self.app.chillerValveWater.set(100)
            self.app.jobs.add_job(
                self.setDelayedPumpState, 
                'interval', 
                seconds=self.config.getint('DEFAULT', 'PUMP_PRIMING_TIME'), 
                id='timerDelayedPump',
                replace_existing=True)
            self.setStatus(currentAction)
        else:
            self.set('false')
            if self.app.jobs.get_job('timerDelayedPump') is not None:
                self.app.jobs.remove_job('timerDelayedPump')
            self.app.boilKettleValveOutlet.set(0)
            self.app.chillerValveWort.set(0)
            self.app.chillerValveWater.set(0)
            self.setStatus(waterActionsEnum.FINISHED)

    def valvesRunKettleToDump(self, state = valveActions.CLOSE):
        if state == valveActions.OPEN:
            currentAction = self.getStatus()
            self.setStatus(waterActionsEnum.BUSY)
            if self.mashTunRecirculation:
                self.valvesRunMashTunToMashTun(state=valveActions.CLOSE, silent=True)
            if self.boilKettleRecirculation:
                self.valvesRunKettleToKettle(state=valveActions.CLOSE, silent=True)
            self.app.outletValveDump.set(100)
            self.app.boilKettleValveOutlet.set(100)
            self.app.jobs.add_job(
                self.setDelayedPumpState, 
                'interval', 
                seconds=self.config.getint('DEFAULT', 'PUMP_PRIMING_TIME'), 
                id='timerDelayedPump',
                replace_existing=True)
            self.setStatus(currentAction)
        else:
            self.set('false')
            if self.app.jobs.get_job('timerDelayedPump') is not None:
                self.app.jobs.remove_job('timerDelayedPump')
            self.app.outletValveDump.set(0)
            self.app.boilKettleValveOutlet.set(0)
            self.setStatus(waterActionsEnum.FINISHED)

    def valvesRunMashTunToDump(self, state = valveActions.CLOSE):
        if state == valveActions.OPEN:
            currentAction = self.getStatus()
            self.setStatus(waterActionsEnum.BUSY)
            if self.mashTunRecirculation:
                self.valvesRunMashTunToMashTun(state=valveActions.CLOSE, silent=True)
            if self.boilKettleRecirculation:
                self.valvesRunKettleToKettle(state=valveActions.CLOSE, silent=True)
            self.app.outletValveDump.set(100)
            self.app.mashTunValveOutlet.set(100)
            self.app.jobs.add_job(
                self.setDelayedPumpState, 
                'interval', 
                seconds=self.config.getint('DEFAULT', 'PUMP_PRIMING_TIME'), 
                id='timerDelayedPump',
                replace_existing=True)
            self.setStatus(currentAction)
        else:
            self.set('false')
            if self.app.jobs.get_job('timerDelayedPump') is not None:
                self.app.jobs.remove_job('timerDelayedPump')
            self.app.outletValveDump.set(0)
            self.app.mashTunValveOutlet.set(0)
            self.setStatus(waterActionsEnum.FINISHED)


    def pumpDaemon(self):

        if self.mashTunRecirculation:
            if self.getStatus() == waterActionsEnum.FINISHED:
                if self.recirculationMashTunFrequencyTime <= 0:
                    self.recirculationMashTunFrequencyTime = self.config.getint('DEFAULT', 'RECIRCULATION_MASHTUN_FREQUENCY_TIME')
                    self.recirculationMashTunTime = self.config.getint('DEFAULT', 'RECIRCULATION_MASHTUN_TIME')
                    if self.recirculationStatus == valveActions.CLOSE:
                        task = threading.Thread(target=self.valvesRunMashTunToMashTun, kwargs=dict(state=valveActions.OPEN, silent=True))
                        task.start()
                else:
                    self.recirculationMashTunFrequencyTime -= self.daemonTime
                    self.recirculationMashTunTime -= self.daemonTime
                    if self.recirculationMashTunTime <= 0 and self.recirculationStatus == valveActions.OPEN:
                        self.recirculationMashTunTime = self.config.getint('DEFAULT', 'RECIRCULATION_MASHTUN_TIME')
                        task = threading.Thread(target=self.valvesRunMashTunToMashTun, kwargs=dict(state=valveActions.CLOSE, silent=True))
                        task.start()

        if self.boilKettleRecirculation:
            if self.getStatus() == waterActionsEnum.FINISHED:
                if self.recirculationBoilKettleFrequencyTime <= 0:
                    self.recirculationBoilKettleFrequencyTime = self.config.getint('DEFAULT', 'RECIRCULATION_BOILKETTLE_FREQUENCY_TIME')
                    self.recirculationBoilKettleTime = self.config.getint('DEFAULT', 'RECIRCULATION_BOILKETTLE_TIME')
                    if self.recirculationStatus == valveActions.CLOSE:
                        task = threading.Thread(target=self.valvesRunKettleToKettle, kwargs=dict(state=valveActions.OPEN, silent=True))
                        task.start()
                else:
                    self.recirculationBoilKettleFrequencyTime -= self.daemonTime
                    self.recirculationBoilKettleTime -= self.daemonTime
                    if self.recirculationBoilKettleTime <= 0 and self.recirculationStatus == valveActions.OPEN:
                        self.recirculationBoilKettleTime = self.config.getint('DEFAULT', 'RECIRCULATION_BOILKETTLE_TIME')
                        task = threading.Thread(target=self.valvesRunKettleToKettle, kwargs=dict(state=valveActions.CLOSE, silent=True))
                        task.start()


        if ((self.app.cooking.isRunning() and self.app.cooking.isPaused()) or 
            (self.app.cleaning.isRunning() and self.app.cleaning.isPaused())):
            self.paused = True
        else:
            self.paused = False
        
        if self.get():
            self.daemonRunningTime += self.daemonTime

        # Fill in the kettle with filtered or non-filtered tap water
        if self.getStatus() == waterActionsEnum.WATER_IN_FILTERED or self.getStatus() == waterActionsEnum.WATER_IN:
            if (self.app.boilKettle.getWaterLevelSetPoint() > 0 and 
                (self.app.boilKettle.getWaterLevel() >= self.app.boilKettle.getWaterLevelSetPoint() or 
                self.app.boilKettle.getWaterLevel() >= self.config.getfloat('BOIL_KETTLE_PINS', 'MAX_WATER_LEVEL'))):

                self.setStatus(waterActionsEnum.BUSY)
                task = threading.Thread(target=self.valvesRunWaterIn, kwargs=dict(state=valveActions.CLOSE))
                task.start()
                self.app.boilKettle.setWaterLevel(0)

        # Rack water from boilkettle to mashtun
        if self.getStatus() == waterActionsEnum.KETTLE_TO_MASHTUN:
            if (self.get()
                and self.daemonRunningTime > 2.0
                and (
                    abs(abs(self.oldBoilKettleWaterLevelValue) - abs(self.app.boilKettle.getWaterLevel())) <= 0.01 or
                    abs(abs(self.oldMashTunWaterLevelValue) - abs(self.app.mashTun.getWaterLevel())) <= 0.01
                    )
                ):
                self.app.logger.info(
                    '[PUMP READING COUNT] DaemonRunningTime: %s. OldBoilKettleWaterLevelValue: %s. BoilKettleWaterLevel: %s. OldBoilKettleWaterLevelValue-BoilKettleWaterLevel<=0.01: %s. oldMashTunWaterLevelValue: %s. MashTunWaterLevel: %s. oldMashTunWaterLevelValue-MashTunWaterLevel<=0.01: %s.', 
                    self.daemonRunningTime, 
                    self.oldBoilKettleWaterLevelValue, 
                    self.app.boilKettle.getWaterLevel(),
                    abs(abs(self.oldBoilKettleWaterLevelValue) - abs(self.app.boilKettle.getWaterLevel())),
                    self.oldMashTunWaterLevelValue, 
                    self.app.mashTun.getWaterLevel(),
                    abs(abs(self.oldMashTunWaterLevelValue) - abs(self.app.mashTun.getWaterLevel()))
                )
                self.waterLevelReadingCount += 1
            else:
                self.waterLevelReadingCount = 0
            self.oldBoilKettleWaterLevelValue = self.app.boilKettle.getWaterLevel()
            self.oldMashTunWaterLevelValue = self.app.mashTun.getWaterLevel()

            if (self.waterLevelReadingCount >= self.config.getint('DEFAULT', 'PUMP_READING_COUNT') or 
                self.app.boilKettle.getWaterLevel() <= 0 or 
                (self.amountToMove > 0 and abs(abs(self.originalBoilKettleWaterLevelValue) - abs(self.oldBoilKettleWaterLevelValue)) >= self.amountToMove) or 
                (self.amountToMove > 0 and abs(abs(self.originalMashTunWaterLevelValue) - abs(self.oldMashTunWaterLevelValue)) >= self.amountToMove) or 
                self.app.mashTun.getWaterLevel() >= self.config.getfloat('MASH_TUN_PINS', 'MAX_WATER_LEVEL')):

                self.setStatus(waterActionsEnum.BUSY)
                self.app.logger.info('[PUMP] Water to move: %s. ReadingCount: %s.', self.amountToMove, self.waterLevelReadingCount)
                self.app.logger.info('[PUMP] Mashtun - OriginalValue: %s. NewValue: %s', self.originalMashTunWaterLevelValue, self.oldMashTunWaterLevelValue)
                self.app.logger.info('[PUMP] Boilkettle - OriginalValue: %s. NewValue: %s', self.originalBoilKettleWaterLevelValue, self.oldBoilKettleWaterLevelValue)
                task = threading.Thread(target=self.valvesRunKettleToMashTun, kwargs=dict(state=valveActions.CLOSE))
                task.start()
                self.oldMashTunWaterLevelValue = 0
                self.oldBoilKettleWaterLevelValue = 0
                self.waterLevelReadingCount = 0
                self.amountToMove = 0
                self.originalMashTunWaterLevelValue = 0
                self.originalBoilKettleWaterLevelValue = 0

        # Rack water from mashtun to boilkettle
        if self.getStatus() == waterActionsEnum.MASHTUN_TO_KETTLE:
            if (self.get()
                and self.daemonRunningTime > 2.0
                and (
                    abs(abs(self.oldBoilKettleWaterLevelValue) - abs(self.app.boilKettle.getWaterLevel())) <= 0.01 or 
                    abs(abs(self.oldMashTunWaterLevelValue) - abs(self.app.mashTun.getWaterLevel())) <= 0.01
                    )
                ):
                self.app.logger.info(
                    '[PUMP READING COUNT] DaemonRunningTime: %s. OldBoilKettleWaterLevelValue: %s. BoilKettleWaterLevel: %s. OldBoilKettleWaterLevelValue-BoilKettleWaterLevel<=0.01: %s. oldMashTunWaterLevelValue: %s. MashTunWaterLevel: %s. oldMashTunWaterLevelValue-MashTunWaterLevel<=0.01: %s.', 
                    self.daemonRunningTime, 
                    self.oldBoilKettleWaterLevelValue, 
                    self.app.boilKettle.getWaterLevel(),
                    abs(abs(self.oldBoilKettleWaterLevelValue) - abs(self.app.boilKettle.getWaterLevel())),
                    self.oldMashTunWaterLevelValue, 
                    self.app.mashTun.getWaterLevel(),
                    abs(abs(self.oldMashTunWaterLevelValue) - abs(self.app.mashTun.getWaterLevel()))
                )
                self.waterLevelReadingCount += 1
            else:
                self.waterLevelReadingCount = 0
            self.oldMashTunWaterLevelValue = self.app.mashTun.getWaterLevel()
            self.oldBoilKettleWaterLevelValue = self.app.boilKettle.getWaterLevel()

            if (self.waterLevelReadingCount >= self.config.getint('DEFAULT', 'PUMP_READING_COUNT') or 
                self.app.mashTun.getWaterLevel() <= 0 or 
                (self.amountToMove > 0 and abs(abs(self.originalMashTunWaterLevelValue) - abs(self.oldMashTunWaterLevelValue)) >= self.amountToMove) or 
                (self.amountToMove > 0 and abs(abs(self.originalBoilKettleWaterLevelValue) - abs(self.oldBoilKettleWaterLevelValue)) >= self.amountToMove) or 
                self.app.boilKettle.getWaterLevel() >= self.config.getfloat('BOIL_KETTLE_PINS', 'MAX_WATER_LEVEL')):

                self.setStatus(waterActionsEnum.BUSY)
                self.app.logger.info('[PUMP] Water to move: %s. ReadingCount: %s.', self.amountToMove, self.waterLevelReadingCount)
                self.app.logger.info('[PUMP] Mashtun - OriginalValue: %s. NewValue: %s', self.originalMashTunWaterLevelValue, self.oldMashTunWaterLevelValue)
                self.app.logger.info('[PUMP] Boilkettle - OriginalValue: %s. NewValue: %s', self.originalBoilKettleWaterLevelValue, self.oldBoilKettleWaterLevelValue)
                task = threading.Thread(target=self.valvesRunMashTunToKettle, kwargs=dict(state=valveActions.CLOSE))
                task.start()
                self.oldMashTunWaterLevelValue = 0
                self.oldBoilKettleWaterLevelValue = 0
                self.waterLevelReadingCount = 0
                self.amountToMove = 0
                self.originalMashTunWaterLevelValue = 0
                self.originalBoilKettleWaterLevelValue = 0

        # Recirculation through mashtun
        if self.getStatus() == waterActionsEnum.MASHTUN_TO_MASHTUN:
            if self.time <= 0:
                self.time = 0
                self.setStatus(waterActionsEnum.BUSY)
                task = threading.Thread(target=self.valvesRunMashTunToMashTun, kwargs=dict(state=valveActions.CLOSE))
                task.start()
            else:
                if not self.paused:
                    self.time -= self.daemonTime

        # Recirculation through boil kettle
        if self.getStatus() == waterActionsEnum.KETTLE_TO_KETTLE:
            if self.time <= 0:
                self.time = 0
                self.setStatus(waterActionsEnum.BUSY)
                task = threading.Thread(target=self.valvesRunKettleToKettle, kwargs=dict(state=valveActions.CLOSE))
                task.start()
            else:
                if not self.paused:
                    self.time -= self.daemonTime

        # Recirculation from boil kettle through chiller
        if self.getStatus() == waterActionsEnum.KETTLE_TO_CHILLER:
            if self.time <= 0:
                self.time = 0
                self.setStatus(waterActionsEnum.BUSY)
                task = threading.Thread(target=self.valvesRunKettleToChiller, kwargs=dict(state=valveActions.CLOSE))
                task.start()
            else:
                if not self.paused:
                    self.time -= self.daemonTime

        # Dump water from boilkettle
        if self.getStatus() == waterActionsEnum.KETTLE_TO_DUMP:
            if (self.get()
                and self.daemonRunningTime > 2.0
                and abs(abs(self.oldBoilKettleWaterLevelValue) - abs(self.app.boilKettle.getWaterLevel())) <= 0.02):
                self.waterLevelReadingCount += 1
            else:
                self.waterLevelReadingCount = 0
            self.oldBoilKettleWaterLevelValue = self.app.boilKettle.getWaterLevel()

            if (self.waterLevelReadingCount >= self.config.getint('DEFAULT', 'PUMP_READING_COUNT') or 
                self.app.boilKettle.getWaterLevel() <= 0 or 
                (self.amountToMove > 0 and abs(abs(self.originalBoilKettleWaterLevelValue) - abs(self.oldBoilKettleWaterLevelValue)) >= self.amountToMove)):

                self.setStatus(waterActionsEnum.BUSY)
                self.app.logger.info('[PUMP] Water to move: %s. ReadingCount: %s.', self.amountToMove, self.waterLevelReadingCount)
                self.app.logger.info('[PUMP] Boilkettle - OriginalValue: %s. NewValue: %s', self.originalBoilKettleWaterLevelValue, self.oldBoilKettleWaterLevelValue)
                task = threading.Thread(target=self.valvesRunKettleToDump, kwargs=dict(state=valveActions.CLOSE))
                task.start()
                self.oldMashTunWaterLevelValue = 0
                self.oldBoilKettleWaterLevelValue = 0
                self.waterLevelReadingCount = 0
                self.amountToMove = 0
                self.originalMashTunWaterLevelValue = 0
                self.originalBoilKettleWaterLevelValue = 0
                

        # Dump water from mashtun
        if self.getStatus() == waterActionsEnum.MASHTUN_TO_DUMP:
            if (self.get()
                and self.daemonRunningTime > 2.0
                and abs(abs(self.oldMashTunWaterLevelValue) - abs(self.app.mashTun.getWaterLevel())) <= 0.02):
                self.waterLevelReadingCount += 1
            else:
                self.waterLevelReadingCount = 0
            self.oldMashTunWaterLevelValue = self.app.mashTun.getWaterLevel()

            if (self.waterLevelReadingCount >= self.config.getint('DEFAULT', 'PUMP_READING_COUNT') or 
                self.app.mashTun.getWaterLevel() <= 0 or 
                (self.amountToMove > 0 and abs(abs(self.originalMashTunWaterLevelValue) - abs(self.oldMashTunWaterLevelValue)) >= self.amountToMove)):

                self.setStatus(waterActionsEnum.BUSY)
                self.app.logger.info('[PUMP] Water to move: %s. ReadingCount: %s.', self.amountToMove, self.waterLevelReadingCount)
                self.app.logger.info('[PUMP] Mashtun - OriginalValue: %s. NewValue: %s', self.originalMashTunWaterLevelValue, self.oldMashTunWaterLevelValue)
                task = threading.Thread(target=self.valvesRunMashTunToDump, kwargs=dict(state=valveActions.CLOSE))
                task.start()
                self.oldMashTunWaterLevelValue = 0
                self.oldBoilKettleWaterLevelValue = 0
                self.waterLevelReadingCount = 0
                self.amountToMove = 0
                self.originalMashTunWaterLevelValue = 0
                self.originalBoilKettleWaterLevelValue = 0





    def moveWater(self, action = waterActionsEnum.FINISHED, amount = 0, time = 0):
        if not isinstance(action, waterActionsEnum):
            raise TypeError("%s attribute must be set to an instance of %s" % (action, waterActionsEnum))

        if ((self.getStatus() == waterActionsEnum.KETTLE_TO_KETTLE  or self.getStatus() == waterActionsEnum.MASHTUN_TO_MASHTUN  or self.getStatus() == waterActionsEnum.KETTLE_TO_CHILLER) 
            and action != waterActionsEnum.FINISHED 
            and action != waterActionsEnum.BUSY):
                self.app.logger.info('[PUMP] Stopping current action: %s. Set new action: %s', self.getStatus(), action)
                self.app.logger.info('[PUMP] Shutting all down in the main thread')
                self.setStatus(waterActionsEnum.BUSY)
                self.shutAllDown()
                return waterActionsEnum.BUSY

        if time > 0:
            self.time = int(time)
        else:
            self.time = 0

        if action == waterActionsEnum.FINISHED:
            self.app.logger.info('[PUMP] Shutting all down in a new thread')
            self.setMashTunRecirculation(False)
            self.setBoilKettleRecirculation(False)
            task = threading.Thread(target=self.shutAllDown)
            task.start()
            return action

        if self.getStatus() == waterActionsEnum.FINISHED:
            self.app.logger.info('[PUMP] Current action: %s. Set new action: %s', self.getStatus(), action)
            self.setStatus(action)

            # Fill in the kettle with filtered or non-filtered tap water
            if action == waterActionsEnum.WATER_IN_FILTERED or action == waterActionsEnum.WATER_IN:
                if amount > 0:
                    self.app.boilKettle.setWaterLevel(max(amount + self.app.boilKettle.getWaterLevel(), self.config.getfloat('DEFAULT', 'SAFE_WATER_LEVEL_FOR_HEATERS')))
                    if self.app.boilKettle.getWaterLevel() < self.app.boilKettle.getWaterLevelSetPoint():
                        task = threading.Thread(target=self.valvesRunWaterIn, kwargs=dict(state=valveActions.OPEN))
                        task.start()

            # Rack water from boilkettle to mashtun
            if action == waterActionsEnum.KETTLE_TO_MASHTUN:
                if amount > 0:
                    self.amountToMove = amount
                else:
                    self.amountToMove = self.app.boilKettle.getWaterLevel()
                self.originalMashTunWaterLevelValue = self.app.mashTun.getWaterLevel()
                self.originalBoilKettleWaterLevelValue = self.app.boilKettle.getWaterLevel()
                task = threading.Thread(target=self.valvesRunKettleToMashTun, kwargs=dict(state=valveActions.OPEN))
                task.start()

            # Rack water from mashtun to boilkettle
            if action == waterActionsEnum.MASHTUN_TO_KETTLE:
                if amount > 0:
                    self.amountToMove = amount
                else:
                    self.amountToMove = self.app.mashTun.getWaterLevel()
                self.originalMashTunWaterLevelValue = self.app.mashTun.getWaterLevel()
                self.originalBoilKettleWaterLevelValue = self.app.boilKettle.getWaterLevel()
                task = threading.Thread(target=self.valvesRunMashTunToKettle, kwargs=dict(state=valveActions.OPEN))
                task.start()

            # Recirculation through boil kettle
            if action == waterActionsEnum.KETTLE_TO_KETTLE:
                task = threading.Thread(target=self.valvesRunKettleToKettle, kwargs=dict(state=valveActions.OPEN))
                task.start()

            # Recirculation from boil kettle through chiller
            if action == waterActionsEnum.KETTLE_TO_CHILLER:
                task = threading.Thread(target=self.valvesRunKettleToChiller, kwargs=dict(state=valveActions.OPEN))
                task.start()

            # Recirculation through CHILLmashtun
            if action == waterActionsEnum.MASHTUN_TO_MASHTUN:
                task = threading.Thread(target=self.valvesRunMashTunToMashTun, kwargs=dict(state=valveActions.OPEN))
                task.start()

            # Recirculation through chiller to cool the wort
            if action == waterActionsEnum.CHILL:
                task = threading.Thread(target=self.valvesRunChill, kwargs=dict(state=valveActions.OPEN))
                task.start()

            # Dump water from boilkettle
            if action == waterActionsEnum.KETTLE_TO_DUMP:
                if amount > 0:
                    self.amountToMove = amount
                else:
                    self.amountToMove = self.app.boilKettle.getWaterLevel()
                    self.originalBoilKettleWaterLevelValue = self.app.boilKettle.getWaterLevel()
                task = threading.Thread(target=self.valvesRunKettleToDump, kwargs=dict(state=valveActions.OPEN))
                task.start()

            # Dump water from mash tun
            if action == waterActionsEnum.MASHTUN_TO_DUMP:
                if amount > 0:
                    self.amountToMove = amount
                else:
                    self.amountToMove = self.app.mashTun.getWaterLevel()
                    self.originalMashTunWaterLevelValue = self.app.mashTun.getWaterLevel()
                task = threading.Thread(target=self.valvesRunMashTunToDump, kwargs=dict(state=valveActions.OPEN))
                task.start()

            return action
        else:
            return waterActionsEnum.BUSY

