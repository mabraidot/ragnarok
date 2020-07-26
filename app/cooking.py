import json
import math
from app.lib.sourcesEnum import soundsEnum, waterActionsEnum, cookingStates


"""
BeerXML Format
==============
RECIPE
------
* BOIL_TIME: duration of boiling expressed in minutes

MASH
----
* SPARGE_TEMP: target temperature for sparging before boiling

MASH STEP
---------
* TYPE: it can be 'Infusion', 'Temperature' or 'Decoction'. Respectively, adding water, raising temp only and draw off some mash for boiling.
* DECOCTION_AMT: if TYPE is 'Decoction', amount of water to draw from mash tun.
* INFUSE_AMOUNT: hot water to add at the start of the step expressed in liters. If it's zero, is a temperature ramp for saccharification or a decoction.
* INFUSE_TEMP: temperature to pre-heat the infused water (format '00.0 C'. Transform to number).
* STEP_TIME: duration of the step after water reach the target step temperature.
* STEP_TEMP: target temperature for the step.
Optional:
* RAMP_TIME: it's an estimated time for the mash to reach the target temperature, based on equipment's hardware.

HOP
---
* TIME: duration of the hop infusion/boiling expressed in minutes, as remaining time of the full mash or boil process.
* USE: step in wich the hop is going to be added, can be 'Mash', 'First Wort', 'Boil', 'Dry Hop' or 'Aroma' (on whirlpool)
Optional:
* AMOUNT: weight of the addition expressed in kilograms.

MISC
----
* TIME: duration of the hop infusion/boiling expressed in minutes, as remaining time of the full mash or boil process.
* USE: step in wich the hop is going to be added, can be 'Mash', 'Boil', 'Primary', 'Secondary' or 'Bottling'
Optional:
* TYPE: can be 'Fining', 'Water Agent', 'Spice', 'Herb', 'Flavor' or 'Other'
* AMOUNT: weight of the addition expressed in kilograms.


CLASS
-----
mash = [{
    state: ('Pending', 'Preheating', 'Running', 'Finished'),
    type: ('Infusion', 'Temperature' or 'Decoction'),
    decoction_amount: 0,
    infuse_amount: 0,
    infuse_temp: 0,
    step_time: 0,
    step_temp: 0
}]
sparge = {
    state: ('Pending', 'Preheating', 'Running', 'Finished'),
    type: 'Sparge',
    infuse_amount: 0,
    infuse_temp: 75,
    step_temp: 75,
    count: 6
}
boil = {
    state: ('Pending', 'Racking', 'Running', 'Finished'),
    step_time: 0,
    step_temp: 105
}
cool = {
    state: ('Pending', 'Running', 'Finished'),
    step_time: 30,
    step_temp: 25
}
mashAdjuncts = [{
    state: ('Pending', 'Running', 'Finished'),
    name: 'name',
    time: 0,
    amount: 0
}]
boilAdjuncts = [{
    state: ('Pending', 'Running', 'Finished'),
    name: 'name',
    time: 0,
    amount: 0
}]

"""
class Cooking:
    def __init__(self, app, config):
        self.app = app
        self.config = config
        self.initialize()
        self.running = False

    def initialize(self):
        self.running = False
        self.paused = False

        self.mashTunTimeSetPoint = 0.0
        self.mashTunTimeProbe = 0.0
        self.boilKettleTimeSetPoint = 0.0
        self.boilKettleTimeProbe = 0.0
        self.app.boilKettle.setWaterLevel(0)
        self.app.mashTun.setWaterLevel(0)

        self.mash = []
        self.mashAdjuncts = []
        self.boilAdjuncts = []
        self.boil = {}
        self.sparge = {}

        self.currentStep = {
            'mash_total_time': 0.0,
            'recipe_id': 0,
            'number': -1,
            'name': 'mash'
        }

        if self.app.jobs.get_job('timerPump') is not None:
            self.app.jobs.remove_job('timerPump')
        if self.app.jobs.get_job('timerHeating') is not None:
            self.app.jobs.remove_job('timerHeating')
        if self.app.jobs.get_job('timerProcess') is not None:
            self.app.jobs.remove_job('timerProcess')
        if self.app.jobs.get_job('timerSavePartialProcess') is not None:
            self.app.jobs.remove_job('timerSavePartialProcess')

    def getCurrentStepName(self):
        return self.currentStep['name']

    def getMashTunTimeSetPoint(self):
        return self.mashTunTimeSetPoint


    def getMashTunTimeProbe(self):
        return self.mashTunTimeProbe


    def getBoilKettleTimeSetPoint(self):
        return self.boilKettleTimeSetPoint


    def getBoilKettleTimeProbe(self):
        return self.boilKettleTimeProbe


    def loadRecipe(self, recipeId):
        recipe = self.app.recipes.getRecipe(recipeId)
        if recipe:
            self.app.recipes.updateCookDate(recipeId)

            self.currentStep['recipe_id'] = int(recipeId)

            if not isinstance(recipe["beer_json"]["RECIPES"]["RECIPE"]["MASH"]["MASH_STEPS"]["MASH_STEP"], list):
                recipe["beer_json"]["RECIPES"]["RECIPE"]["MASH"]["MASH_STEPS"]["MASH_STEP"] = [recipe["beer_json"]["RECIPES"]["RECIPE"]["MASH"]["MASH_STEPS"]["MASH_STEP"]]
            mashSteps = recipe["beer_json"]["RECIPES"]["RECIPE"]["MASH"]["MASH_STEPS"]["MASH_STEP"]
            for step in mashSteps:
                self.mash.append({
                    'state': cookingStates.PENDING,
                    'type': step['TYPE'],
                    'decoction_amount': float("{0:.2f}".format(float(step['DECOCTION_AMT'].split(" ")[0]))),
                    'infuse_amount': float("{0:.2f}".format(float(step['INFUSE_AMOUNT']))),
                    'infuse_temp': float("{0:.2f}".format(float(step['INFUSE_TEMP'].split(" ")[0]))),
                    'step_time': float("{0:.2f}".format(float(step['STEP_TIME']))),
                    'step_temp': float("{0:.2f}".format(float(step['STEP_TEMP'])))
                })
                self.currentStep['mash_total_time'] += float("{0:.2f}".format(float(step['STEP_TIME'])))

            if not isinstance(recipe["beer_json"]["RECIPES"]["RECIPE"]["HOPS"]["HOP"], list):
                recipe["beer_json"]["RECIPES"]["RECIPE"]["HOPS"]["HOP"] = [recipe["beer_json"]["RECIPES"]["RECIPE"]["HOPS"]["HOP"]]
            if not isinstance(recipe["beer_json"]["RECIPES"]["RECIPE"]["MISCS"]["MISC"], list):
                recipe["beer_json"]["RECIPES"]["RECIPE"]["MISCS"]["MISC"] = [recipe["beer_json"]["RECIPES"]["RECIPE"]["MISCS"]["MISC"]]
            hopAdjuncts = recipe["beer_json"]["RECIPES"]["RECIPE"]["HOPS"]["HOP"]
            hopAdjuncts += recipe["beer_json"]["RECIPES"]["RECIPE"]["MISCS"]["MISC"]
            hopAdjuncts = sorted(hopAdjuncts, key = lambda i: float(i['TIME']), reverse=True)
            for step in hopAdjuncts:
                if step['USE'] == 'Mash':
                    self.mashAdjuncts.append({
                        'state': cookingStates.PENDING,
                        'name': step['NAME'],
                        'time': float("{0:.2f}".format(float(step['TIME']))),
                        'amount': float("{0:.5f}".format(float(step['AMOUNT'])))
                    })
                elif step['USE'] == 'First Wort':
                    self.mashAdjuncts.append({
                        'state': cookingStates.PENDING,
                        'name': step['NAME'],
                        'time': 0.1,
                        'amount': float("{0:.5f}".format(float(step['AMOUNT'])))
                    })
                elif step['USE'] == 'Boil' or step['USE'] == 'Aroma':
                    self.boilAdjuncts.append({
                        'state': cookingStates.PENDING,
                        'name': step['NAME'],
                        'time': float("{0:.2f}".format(float(step['TIME']))),
                        'amount': float("{0:.5f}".format(float(step['AMOUNT'])))
                    })

            self.sparge =  {
                'state': cookingStates.PENDING,
                'type': 'Sparge',
                'infuse_amount': self.config.getfloat('DEFAULT', 'SPARGE_INFUSE_AMOUNT'),
                'infuse_temp': float("{0:.2f}".format(float(recipe["beer_json"]["RECIPES"]["RECIPE"]["MASH"]["SPARGE_TEMP"]))),
                'step_temp': float("{0:.2f}".format(float(recipe["beer_json"]["RECIPES"]["RECIPE"]["MASH"]["SPARGE_TEMP"]))),
                'count': self.config.getfloat('DEFAULT', 'SPARGE_CYCLES_COUNT')
            }

            self.boil =  {
                'state': cookingStates.PENDING,
                'step_time': float("{0:.2f}".format(float(recipe["beer_json"]["RECIPES"]["RECIPE"]["BOIL_TIME"]))),
                'step_temp': self.config.getfloat('DEFAULT', 'BOIL_TEMPERATURE')
            }

            self.cool =  {
                'state': cookingStates.PENDING,
                'step_time': self.config.getfloat('DEFAULT', 'COOL_TIME'),
                'step_temp': self.config.getfloat('DEFAULT', 'COOL_TEMPERATURE')
            }



    def decimalTotime(self, decimalTime):
        minutes = int(decimalTime)
        seconds = math.floor((decimalTime - minutes) * 60)
        time = str("{:02d}".format(minutes)) + ':' + str("{:02d}".format(seconds))
        return time


    def notifyAdjuncts(self):
        if self.currentStep['name'] == 'mash':
            for adjunct in self.mashAdjuncts:
                if adjunct['state'] == cookingStates.PENDING and abs(adjunct['time'] - self.currentStep['mash_total_time']) <= 1/60:
                    # NOTIFY
                    adjunct['state'] = cookingStates.FINISHED
                    self.app.ws.setLog({
                        self.config.get('DEFAULT', 'LOG_NOTICE_ADJUNCTS_LABEL'): 
                        '[' + self.decimalTotime(adjunct['time']) + '] Add ' + str(adjunct['amount'] * 1000) + ' grams of ' + adjunct['name'].upper()
                    })
                    self.app.sound.play(soundsEnum.ALARM, 25)
                    self.app.logger.info('[MASH_ADJUNCTS] %s', adjunct)

        elif self.currentStep['name'] == 'boil':
            for adjunct in self.boilAdjuncts:
                if adjunct['state'] == cookingStates.PENDING and abs(adjunct['time'] - self.boilKettleTimeProbe) <= 1/60:
                    # NOTIFY
                    adjunct['state'] = cookingStates.FINISHED
                    self.app.ws.setLog({
                        self.config.get('DEFAULT', 'LOG_NOTICE_ADJUNCTS_LABEL'): 
                        '[' + self.decimalTotime(adjunct['time']) + '] Add ' + str(adjunct['amount'] * 1000) + ' grams of ' + adjunct['name'].upper()
                    })
                    self.app.sound.play(soundsEnum.ALARM, 25)
                    self.app.logger.info('[BOIL_ADJUNCTS] %s', adjunct)



    def mayNextStepStartPreHeating(self):
        if self.currentStep['name'] == 'mash': 
            if self.currentStep['number'] + 1 < len(self.mash):
                step = self.mash[self.currentStep['number'] + 1]
                if step['type'] == 'Infusion' and step['state'] == cookingStates.PENDING:
                    if (
                        self.mashTunTimeProbe < self.config.getfloat('DEFAULT', 'NEXT_STEP_PRE_HEATING_TIME') or
                        self.mash[self.currentStep['number']]['step_time'] < self.config.getfloat('DEFAULT', 'NEXT_STEP_PRE_HEATING_TIME')
                    ):
                        return True
            elif self.sparge['state'] == cookingStates.PENDING:
                if (
                    self.mashTunTimeProbe < self.config.getfloat('DEFAULT', 'NEXT_STEP_PRE_HEATING_TIME') or
                    self.mash[self.currentStep['number']]['step_time'] < self.config.getfloat('DEFAULT', 'NEXT_STEP_PRE_HEATING_TIME')
                ):
                    return True
        return False


    def rackMushTunRest(self):
        if self.currentStep['name'] == 'boil':
            if self.boil['state'] != cookingStates.RACKING and self.app.boilKettle.getTemperature() > self.boil['step_temp'] - self.config.getfloat('DEFAULT', 'TEMP_LEFT_RACK_MASHTUN_REST'):
                state = self.app.pump.moveWater(action=waterActionsEnum.MASHTUN_TO_KETTLE)
                self.app.logger.info('[RACKING MASHTUN_TO_KETTLE] %s', state)
                if state != waterActionsEnum.BUSY:
                    self.boil['state'] = cookingStates.RACKING
                    self.app.logger.info('[BOIL] RACKING %s', self.boil)


    def timerProcess(self):
        if self.currentStep['name'] == 'mash':
            if self.mashTunTimeProbe > 0:
                if not self.isPaused():
                    self.mashTunTimeProbe -= 1/60
                    self.currentStep['mash_total_time'] -= 1/60
                    if self.mayNextStepStartPreHeating():
                        if self.currentStep['number'] + 1 < len(self.mash):
                            step = self.mash[self.currentStep['number'] + 1]
                        else:
                            step = self.sparge
                        self.startStep(step, True)
                    self.notifyAdjuncts()
            else:
                self.mashTunTimeProbe = 0
                self.mash[self.currentStep['number']]['state'] = cookingStates.FINISHED
                self.app.jobs.remove_job('timerProcess')
                self.setNextStep()
        elif self.currentStep['name'] == 'boil':
            if self.boilKettleTimeProbe > 0:
                if not self.isPaused():
                    self.boilKettleTimeProbe -= 1/60
                    self.notifyAdjuncts()
            else:
                self.boilKettleTimeProbe = 0
                self.app.pump.setBoilKettleRecirculation(False)
                self.app.pump.moveWater(waterActionsEnum.FINISHED)
                self.app.boilKettle.stopHeating()
                self.boil['state'] = cookingStates.FINISHED
                self.currentStep['number'] = -1
                self.currentStep['name'] = 'paused'
                self.app.sound.play(soundsEnum.SUCCESS)
                self.app.jobs.remove_job('timerProcess')
        elif self.currentStep['name'] == 'cool':
            if self.boilKettleTimeProbe > 0:
                if not self.isPaused():
                    self.boilKettleTimeProbe -= 1/60
            if self.app.boilKettle.getTemperature() < self.cool['step_temp'] or self.boilKettleTimeProbe <= 0:
                self.app.pump.moveWater(action=waterActionsEnum.FINISHED)
                self.cool['state'] = cookingStates.FINISHED
                self.currentStep['number'] = -1
                self.currentStep['name'] = 'finish'
                self.app.jobs.remove_job('timerProcess')
                self.app.sound.play(soundsEnum.SUCCESS)
                self.setNextStep()


    def timerPump(self):
        if self.currentStep['name'] == 'mash' and self.currentStep['number'] >= 0 and self.currentStep['number'] < len(self.mash):
            step = self.mash[self.currentStep['number']]
            if step['type'] == 'Infusion':
                if self.app.pump.getStatus() == waterActionsEnum.FINISHED and self.app.mashTun.getTemperature() >= step['step_temp']:
                    self.app.pump.setMashTunRecirculation(True)
                    self.app.jobs.add_job(self.timerProcess, 'interval', seconds=1, id='timerProcess', replace_existing=True)
                    self.app.jobs.remove_job('timerPump')
                else:
                    self.app.mashTun.heatToTemperature(step['step_temp'])
        elif self.currentStep['name'] == 'sparge':
            self.app.pump.setMashTunRecirculation(False)
            if self.app.pump.getStatus() == waterActionsEnum.FINISHED:
                self.setNextStep()
                self.app.jobs.remove_job('timerPump')



    def getMashWaterLevelSoFar(self, stepNumber):
        totalWater = 0
        for i in range(stepNumber+1):
            totalWater += self.mash[i]['infuse_amount']
        return totalWater
        

    def timerHeating(self, preHeating = False):
        if self.currentStep['name'] == 'mash':
            step = self.mash[self.currentStep['number']]
            if step['type'] == 'Infusion':
                targetWaterLevelSoFar = self.getMashWaterLevelSoFar(self.currentStep['number'])
                if self.app.boilKettle.getTemperature() >= step['infuse_temp'] or (not preHeating and self.app.mashTun.getWaterLevel() >= targetWaterLevelSoFar):
                    state = self.app.pump.moveWater(action=waterActionsEnum.KETTLE_TO_MASHTUN)
                    if state != waterActionsEnum.BUSY:
                        self.app.boilKettle.stopHeating()
                        self.app.mashTun.heatToTemperature(step['step_temp'])
                        self.app.jobs.add_job(self.timerPump, 'interval', seconds=1, id='timerPump', replace_existing=True)
                        if self.app.jobs.get_job('timerHeating') is not None:
                            self.app.jobs.remove_job('timerHeating')
            if step['type'] == 'Temperature':
                if self.app.mashTun.getTemperature() >= step['step_temp']:
                    self.app.jobs.add_job(self.timerProcess, 'interval', seconds=1, id='timerProcess', replace_existing=True)
                    if self.app.jobs.get_job('timerHeating') is not None:
                        self.app.jobs.remove_job('timerHeating')
        elif self.currentStep['name'] == 'boil':
            if self.app.boilKettle.getTemperature() >= self.boil['step_temp']:
                self.app.boilKettle.heatToTemperature(self.boil['step_temp'] + 10)
                self.app.jobs.add_job(self.timerProcess, 'interval', seconds=1, id='timerProcess', replace_existing=True)
                if self.app.jobs.get_job('timerHeating') is not None:
                    self.app.jobs.remove_job('timerHeating')
            else:
                self.rackMushTunRest()
        elif self.currentStep['name'] == 'sparge':
            step = self.sparge
            if self.app.boilKettle.getTemperature() >= step['infuse_temp']:
                if int(step['count']) % 2 != 0:
                    state = self.app.pump.moveWater(action=waterActionsEnum.MASHTUN_TO_KETTLE, amount=step['infuse_amount'])
                else:
                    state = self.app.pump.moveWater(action=waterActionsEnum.KETTLE_TO_MASHTUN, amount=step['infuse_amount'])
                if state != waterActionsEnum.BUSY:
                    self.app.jobs.add_job(self.timerPump, 'interval', seconds=1, id='timerPump', replace_existing=True)
                    if self.app.jobs.get_job('timerHeating') is not None:
                        self.app.jobs.remove_job('timerHeating')
                else:
                    self.app.logger.info('[SPARGE ATTEMPT] %s', state)



    def startStep(self, step, preHeating = False):
        if step['type'] == 'Infusion' and step['infuse_amount'] > 0:

            if preHeating or (( not preHeating or self.app.boilKettle.getTemperature() < step['infuse_temp'] ) and self.app.mashTun.getWaterLevel() <= 0.5 ):
                state = self.app.pump.moveWater(action=waterActionsEnum.WATER_IN_FILTERED, amount=step['infuse_amount'])
                if state != waterActionsEnum.BUSY:
                    step['state'] = cookingStates.PREHEATING
                    self.app.boilKettle.heatToTemperature(step['infuse_temp'])
            
            if not preHeating:
                self.app.boilKettle.heatToTemperature(step['infuse_temp'])
                self.app.jobs.add_job(self.timerHeating, 'interval', seconds=1, args=[preHeating], id='timerHeating', replace_existing=True)
                
                if self.app.mashTun.getWaterLevel() > 1:
                    self.app.pump.setMashTunRecirculation(True)

        elif step['type'] == 'Temperature' and not preHeating:
            self.app.mashTun.heatToTemperature(step['step_temp'])
            self.app.jobs.add_job(self.timerHeating, 'interval', seconds=1, id='timerHeating', replace_existing=True)
            self.app.pump.setMashTunRecirculation(True)

        elif step['type'] == 'Decoction' and not preHeating:
            # TODO: handle the decoction process
            self.setNextStep()

        elif step['type'] == 'Sparge' and step['infuse_amount'] > 0 and preHeating:
            state = self.app.pump.moveWater(action=waterActionsEnum.WATER_IN_FILTERED, amount=step['infuse_amount'])
            if state != waterActionsEnum.BUSY:
                step['state'] = cookingStates.PREHEATING
                self.app.boilKettle.heatToTemperature(step['infuse_temp'])



    def setNextStep(self):
        if self.currentStep['recipe_id'] > 0:
            self.currentStep['number'] += 1
            if self.currentStep['name'] == 'mash':
                if self.currentStep['number'] < len(self.mash):
                    step = self.mash[self.currentStep['number']]
                    self.startStep(step, False)

                    self.mashTunTimeSetPoint = step['step_time']
                    if self.mashTunTimeProbe == 0:
                        self.mashTunTimeProbe = step['step_time']
                    self.mash[self.currentStep['number']]['state'] = cookingStates.RUNNING
                    self.app.logger.info('[STEP-MASH: '+str(self.currentStep['number'])+'] %s', self.mash[self.currentStep['number']])

                else:
                    self.currentStep['number'] = -1
                    self.currentStep['name'] = 'sparge'
                    self.setNextStep()

            elif self.currentStep['name'] == 'sparge':
                step = self.sparge
                if step['count'] <= 0:
                    self.currentStep['number'] = -1
                    self.currentStep['name'] = 'boil'
                    if self.app.jobs.get_job('timerHeating') is not None:
                        self.app.jobs.remove_job('timerHeating')
                    self.setNextStep()
                    return
                step['count'] -= 1
                self.app.jobs.add_job(self.timerHeating, 'interval', seconds=1, id='timerHeating', replace_existing=True)
                self.app.logger.info('[STEP-SPARGE: '+str(step['count'])+'] %s', step)

            elif self.currentStep['name'] == 'boil':
                step = self.boil
                self.boilKettleTimeSetPoint = step['step_time']
                if self.boilKettleTimeProbe == 0:
                    self.boilKettleTimeProbe = step['step_time']
                self.boil['state'] = cookingStates.RUNNING
                self.app.mashTun.stopHeating()
                self.app.pump.moveWater(action=waterActionsEnum.MASHTUN_TO_KETTLE)
                self.app.boilKettle.heatToTemperature(step['step_temp'])
                self.app.jobs.add_job(self.timerHeating, 'interval', seconds=1, id='timerHeating', replace_existing=True)
                self.app.pump.setMashTunRecirculation(False)
                self.app.pump.setBoilKettleRecirculation(True)
                self.app.logger.info('[BOIL] %s', self.boil)

            elif self.currentStep['name'] == 'paused':

                self.currentStep['name'] = 'cool'
                step = self.cool
                self.boilKettleTimeSetPoint = 0
                self.cool['state'] = cookingStates.RUNNING
                self.boilKettleTimeSetPoint = step['step_time']
                self.boilKettleTimeProbe = step['step_time']
                self.app.boilKettle.stopHeating()
                self.app.pump.moveWater(action=waterActionsEnum.CHILL)
                self.app.jobs.add_job(self.timerProcess, 'interval', seconds=1, id='timerProcess', replace_existing=True)
                self.app.logger.info('[COOL] %s', self.cool)

            elif self.currentStep['name'] == 'finish':
                self.stop()
                self.app.ws.setLog({
                    self.config.get('DEFAULT', 'LOG_NOTICE_PERSISTENT_LABEL'): 
                    'The cooking process has finished!. Please dump the wort manually.'
                })
                self.app.logger.info('[END-COOK] %s', self.currentStep)
            self.app.logger.info('[CURRENT_STEP] %s', self.currentStep)
        else:
            return


    def isRunning(self):
        return self.running


    def isPaused(self):
        return self.paused


    def pause(self):
        self.paused = not self.paused
        if self.paused:
            self.app.logger.info('[COOKING PAUSED]')
        else:
            self.app.logger.info('[COOKING RESUMED]')


    def stop(self):
        from app.recipes import Recipes
        self.app.recipes = Recipes(self.app, self.config)
        self.app.recipes.deleteUnfinishedRecipe()

        self.app.mashTun.stopHeating()
        self.app.boilKettle.stopHeating()
        self.app.pump.moveWater(action=waterActionsEnum.FINISHED)
        self.app.logger.info('===============================================================================')
        self.initialize()


    def timerSavePartialProcess(self):
        from app.recipes import Recipes
        self.app.recipes = Recipes(self.app, self.config)
        self.app.recipes.updateUnfinishedRecipe(self.currentStep['recipe_id'], self.currentStep['name'], 
            self.currentStep['number'], self.currentStep['mash_total_time'], self.app.mashTun.getWaterLevel(), 
            self.mashTunTimeProbe, self.app.boilKettle.getWaterLevel(), self.boilKettleTimeProbe)


    def start(self, recipeId):
        self.initialize()
        self.app.pump.shutAllDown()
        self.app.mashTun.tare()
        self.app.boilKettle.tare()
        self.running = True
        self.loadRecipe(recipeId)
        self.app.jobs.add_job(
            self.timerSavePartialProcess, 'interval', 
            seconds=self.config.getint('DEFAULT', 'SAVING_PARTIAL_PROCESS_INTERVAL'), 
            id='timerSavePartialProcess', replace_existing=True)
        self.setNextStep()


    def resume(self, recipeId):
        self.initialize()
        self.app.mashTun.tare()
        self.app.boilKettle.tare()
        self.loadRecipe(recipeId)

        unfinishedRecipe = self.app.recipes.getUnfinishedRecipe()

        self.currentStep = {
            'mash_total_time': float(unfinishedRecipe['mash_total_time']),
            'recipe_id': int(recipeId),
            'number': int(unfinishedRecipe['process_number']),
            'name': unfinishedRecipe['process_name']
        }
        
        self.app.mashTun.setPriorWaterLevel(float(unfinishedRecipe['mashtun_water_level']))
        self.mashTunTimeProbe = float(unfinishedRecipe['mashtun_time_probe'])
        self.app.boilKettle.setPriorWaterLevel(float(unfinishedRecipe['boilkettle_water_level']))
        self.boilKettleTimeProbe = float(unfinishedRecipe['boilkettle_time_probe'])
        
        self.currentStep['number'] -= 1
        self.running = True
        self.app.jobs.add_job(
            self.timerSavePartialProcess, 'interval', 
            seconds=self.config.getint('DEFAULT', 'SAVING_PARTIAL_PROCESS_INTERVAL'), 
            id='timerSavePartialProcess', replace_existing=True)
        self.setNextStep()
