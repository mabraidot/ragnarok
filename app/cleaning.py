from app.lib.sourcesEnum import waterActionsEnum, cleaningProgramsActions, cookingStates


"""
clean[{
    state: ('Pending', 'Preheating', 'Running', 'Finished'),
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


    def loadProgram(self, program=cleaningProgramsActions.SHORT):
        if program == cleaningProgramsActions.SHORT:
            self.currentStep['program'] = cleaningProgramsActions.SHORT
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


    def setNextStep(self):
        self.currentStep['number'] += 1
        if self.currentStep['number'] < len(self.clean):
            step = self.clean[self.currentStep['number']]
            
            # start step

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
