from app.lib.sourcesEnum import waterActionsEnum, cleaningProgramsActions, cookingStates


"""
clean[{
    state: ('Pending', 'Dumping', 'Running', 'Finished'),
    type: ('BoilKettle', 'MashTun'),
    water_amount: 0,
    kettle_recirculation_time: 0,
    chiller_recirculation_time: 0,
    step_temp: 0,
    dump: (True, False)
}]
"""
class Cleaning:
    def __init__(self, app, config):
        self.app = app
        self.config = config
        self.initialize()
        self.running = False

    def initialize(self):
        self.running = False

        self.mashTunTimeSetPoint = 0.0
        self.mashTunTimeProbe = 0.0
        self.boilKettleTimeSetPoint = 0.0
        self.boilKettleTimeProbe = 0.0
        self.app.boilKettle.setWaterLevel(0)
        self.app.mashTun.setWaterLevel(0)

        self.clean = []
        self.currentStep = {
            'number': -1,
            'program': cleaningProgramsActions.SHORT
        }

    def getMashTunTimeSetPoint(self):
        return self.mashTunTimeSetPoint


    def getMashTunTimeProbe(self):
        return self.mashTunTimeProbe


    def getBoilKettleTimeSetPoint(self):
        return self.boilKettleTimeSetPoint


    def getBoilKettleTimeProbe(self):
        return self.boilKettleTimeProbe


    def loadProgram(self, program=cleaningProgramsActions.SHORT):
        if program == cleaningProgramsActions.SHORT:
            self.currentStep['program'] = cleaningProgramsActions.SHORT
            self.clean.append({
                'state': cookingStates.PENDING,
                'type': 'BoilKettle',
                'water_amount': 13,
                'kettle_recirculation_time': 0.2,
                'chiller_recirculation_time': 0.2,
                'step_temp': 15,
                'dump': False,
            })
            self.clean.append({
                'state': cookingStates.PENDING,
                'type': 'MashTun',
                'water_amount': 4,
                'kettle_recirculation_time': 0.1,
                'chiller_recirculation_time': 0,
                'step_temp': 15,
                'dump': True,
            })
            # self.clean.append({
            #     'state': cookingStates.PENDING,
            #     'type': 'BoilKettle',
            #     'water_amount': 4,
            #     'kettle_recirculation_time': 1,
            #     'chiller_recirculation_time': 1,
            #     'step_temp': 50,
            #     'dump': True,
            # })
            # self.clean.append({
            #     'state': cookingStates.PENDING,
            #     'type': 'MashTun',
            #     'water_amount': 4,
            #     'kettle_recirculation_time': 1,
            #     'chiller_recirculation_time': 0,
            #     'step_temp': 50,
            #     'dump': True,
            # })

        if program == cleaningProgramsActions.SANITIZATION:
            self.currentStep['program'] = cleaningProgramsActions.SANITIZATION
            self.clean.append({
                'state': cookingStates.PENDING,
                'type': 'BoilKettle',
                'water_amount': 5,
                'kettle_recirculation_time': 2,
                'chiller_recirculation_time': 2,
                'step_temp': 80,
                'dump': False,
            })
            self.clean.append({
                'state': cookingStates.PENDING,
                'type': 'MashTun',
                'water_amount': 5,
                'kettle_recirculation_time': 2,
                'chiller_recirculation_time': 0,
                'step_temp': 80,
                'dump': True,
            })

        if program == cleaningProgramsActions.FULL:
            self.currentStep['program'] = cleaningProgramsActions.FULL
            self.clean.append({
                'state': cookingStates.PENDING,
                'type': 'BoilKettle',
                'water_amount': 4,
                'kettle_recirculation_time': 1,
                'chiller_recirculation_time': 1,
                'step_temp': 50,
                'dump': True,
            })
            self.clean.append({
                'state': cookingStates.PENDING,
                'type': 'MashTun',
                'water_amount': 4,
                'kettle_recirculation_time': 1,
                'chiller_recirculation_time': 0,
                'step_temp': 50,
                'dump': True,
            })
            self.clean.append({
                'state': cookingStates.PENDING,
                'type': 'BoilKettle',
                'water_amount': 6,
                'kettle_recirculation_time': 2,
                'chiller_recirculation_time': 3,
                'step_temp': 80,
                'dump': False,
            })
            self.clean.append({
                'state': cookingStates.PENDING,
                'type': 'MashTun',
                'water_amount': 6,
                'kettle_recirculation_time': 2,
                'chiller_recirculation_time': 0,
                'step_temp': 80,
                'dump': True,
            })
            self.clean.append({
                'state': cookingStates.PENDING,
                'type': 'BoilKettle',
                'water_amount': 5,
                'kettle_recirculation_time': 2,
                'chiller_recirculation_time': 2,
                'step_temp': 50,
                'dump': False,
            })
            self.clean.append({
                'state': cookingStates.PENDING,
                'type': 'MashTun',
                'water_amount': 5,
                'kettle_recirculation_time': 2,
                'chiller_recirculation_time': 0,
                'step_temp': 50,
                'dump': True,
            })


    def timerProcess(self):
        step = self.clean[self.currentStep['number']]
        if step['type'] == 'MashTun':
            if self.mashTunTimeProbe > 0:
                self.mashTunTimeProbe -= 1/60
            else:
                self.mashTunTimeProbe = 0
                self.app.mashTun.stopHeating()
                if step['state'] != cookingStates.DUMPING:
                    self.app.pump.moveWater(action=waterActionsEnum.FINISHED)
                if step['dump'] and step['state'] != cookingStates.DUMPING:
                    step['state'] = cookingStates.DUMPING
                    self.app.pump.moveWater(action=waterActionsEnum.MASHTUN_TO_DUMP)
                elif self.app.pump.getStatus() == waterActionsEnum.FINISHED:
                    self.app.jobs.remove_job('timerProcess')
                    self.clean[self.currentStep['number']]['state'] = cookingStates.FINISHED
                    self.setNextStep()

        if step['type'] == 'BoilKettle':
            if self.boilKettleTimeProbe > 0:
                self.boilKettleTimeProbe -= 1/60
                if step['chiller_recirculation_time'] > 0 and self.boilKettleTimeProbe <= step['kettle_recirculation_time'] and (self.app.pump.getStatus() == waterActionsEnum.KETTLE_TO_CHILLER or self.app.pump.getStatus() == waterActionsEnum.FINISHED):
                    self.app.pump.moveWater(action=waterActionsEnum.FINISHED)
                    self.app.pump.moveWater(action=waterActionsEnum.KETTLE_TO_KETTLE, time=step['kettle_recirculation_time'] * 60)
            else:
                self.boilKettleTimeProbe = 0
                self.app.boilKettle.stopHeating()
                if step['state'] != cookingStates.DUMPING:
                    self.app.pump.moveWater(action=waterActionsEnum.FINISHED)
                if step['dump'] and step['state'] != cookingStates.DUMPING:
                    step['state'] = cookingStates.DUMPING
                    self.app.pump.moveWater(action=waterActionsEnum.KETTLE_TO_DUMP)
                elif self.app.pump.getStatus() == waterActionsEnum.FINISHED:
                    self.app.jobs.remove_job('timerProcess')
                    self.clean[self.currentStep['number']]['state'] = cookingStates.FINISHED
                    self.setNextStep()


    def timerHeating(self):
        step = self.clean[self.currentStep['number']]
        if step['type'] == 'MashTun':
            if self.app.mashTun.getTemperature() >= step['step_temp'] and self.app.pump.getStatus() == waterActionsEnum.FINISHED:
                self.app.jobs.add_job(self.timerProcess, 'interval', seconds=1, id='timerProcess', replace_existing=True)
                if step['kettle_recirculation_time'] > 0:
                    self.app.pump.moveWater(action=waterActionsEnum.MASHTUN_TO_MASHTUN, time=step['kettle_recirculation_time'] * 60)
                self.app.jobs.remove_job('timerHeating')
            else:
                if self.app.boilKettle.getWaterLevel() >= step['water_amount'] and self.app.pump.getStatus() == waterActionsEnum.FINISHED:
                    self.app.boilKettle.stopHeating()
                    self.app.pump.moveWater(action=waterActionsEnum.KETTLE_TO_MASHTUN)
                self.app.mashTun.heatToTemperature(step['step_temp'])

        elif step['type'] == 'BoilKettle':
            if self.app.boilKettle.getTemperature() >= step['step_temp'] and self.app.pump.getStatus() == waterActionsEnum.FINISHED:
                self.app.jobs.remove_job('timerHeating')
                self.app.jobs.add_job(self.timerProcess, 'interval', seconds=1, id='timerProcess', replace_existing=True)
                if step['chiller_recirculation_time'] > 0:
                    self.app.pump.moveWater(action=waterActionsEnum.KETTLE_TO_CHILLER, time=step['kettle_recirculation_time'] * 60)
                elif step['kettle_recirculation_time'] > 0:
                    self.app.pump.moveWater(action=waterActionsEnum.KETTLE_TO_KETTLE, time=step['kettle_recirculation_time'] * 60)
            else:
                self.app.boilKettle.heatToTemperature(step['step_temp'])


    def startStep(self, step):
        if self.currentStep['number'] > 0 and not self.clean[self.currentStep['number']-1]['dump']:
            if step['type'] == 'BoilKettle' and self.clean[self.currentStep['number']-1]['type'] == 'MashTun':
                self.app.pump.moveWater(action=waterActionsEnum.MASHTUN_TO_KETTLE)
                self.app.mashTun.stopHeating()
                self.app.boilKettle.heatToTemperature(step['step_temp'])
            elif step['type'] == 'MashTun' and self.clean[self.currentStep['number']-1]['type'] == 'BoilKettle':
                self.app.pump.moveWater(action=waterActionsEnum.KETTLE_TO_MASHTUN)
                self.app.boilKettle.stopHeating()
                self.app.mashTun.heatToTemperature(step['step_temp'])
            else:
                self.app.pump.moveWater(action=waterActionsEnum.WATER_IN_FILTERED, amount=step['water_amount'])
                self.app.boilKettle.heatToTemperature(step['step_temp'])
        else:
            self.app.pump.moveWater(action=waterActionsEnum.WATER_IN_FILTERED, amount=step['water_amount'])
            self.app.boilKettle.heatToTemperature(step['step_temp'])

        self.app.jobs.add_job(self.timerHeating, 'interval', seconds=1, id='timerHeating', replace_existing=True)


    def setNextStep(self):
        self.currentStep['number'] += 1
        if self.currentStep['number'] < len(self.clean):
            step = self.clean[self.currentStep['number']]

            self.startStep(step)

            if step['type'] == 'MashTun':
                self.mashTunTimeSetPoint = step['kettle_recirculation_time']
                if self.mashTunTimeProbe == 0:
                    self.mashTunTimeProbe = self.mashTunTimeSetPoint
            elif step['type'] == 'BoilKettle':
                self.boilKettleTimeSetPoint = step['kettle_recirculation_time'] + step['chiller_recirculation_time']
                if self.boilKettleTimeProbe == 0:
                    self.boilKettleTimeProbe = self.boilKettleTimeSetPoint
            step['state'] = cookingStates.RUNNING
            self.app.logger.info('[STEP-CLEAN: '+str(self.currentStep['number'])+'] %s', step)

        else:
            self.stop()
            self.app.ws.setLog({
                self.config.get('DEFAULT', 'LOG_NOTICE_PERSISTENT_LABEL'): 
                'The cleaning process has finished!.'
            })
            self.app.logger.info('[END] %s', self.currentStep)


    def isRunning(self):
        return self.running


    def stop(self):
        self.app.mashTun.stopHeating()
        self.app.boilKettle.stopHeating()
        self.app.pump.moveWater(action=waterActionsEnum.FINISHED)
        self.initialize()

    def startShort(self):
        self.initialize()
        self.app.pump.shutAllDown()
        self.app.mashTun.tare()
        self.app.boilKettle.tare()
        self.running = True
        self.loadProgram(cleaningProgramsActions.SHORT)
        self.setNextStep()

    def startSanitization(self):
        self.initialize()
        self.app.pump.shutAllDown()
        self.app.mashTun.tare()
        self.app.boilKettle.tare()
        self.running = True
        self.loadProgram(cleaningProgramsActions.SANITIZATION)
        self.setNextStep()

    def startFull(self):
        self.initialize()
        self.app.pump.shutAllDown()
        self.app.mashTun.tare()
        self.app.boilKettle.tare()
        self.running = True
        self.loadProgram(cleaningProgramsActions.FULL)
        self.setNextStep()
