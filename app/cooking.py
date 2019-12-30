import json
from app.hardware.sourcesEnum import waterActionsEnum

"""
BeerXML Format
==============
RECIPE
------
* BOIL_TIME: duration of boiling expressed in minutes

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
    state: ('Pending', 'Running', 'Finished'),
    type: ('Infusion', 'Temperature' or 'Decoction'),
    decoction_amount: 0,
    infuse_amount: 0,
    infuse_temp: 0,
    step_time: 0,
    step_temp: 0
}]
boil = {
    state: ('Pending', 'Running', 'Finished'),
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

    def initialize(self):
        self.mashTunTimeSetPoint = 0.0
        self.mashTunTimeProbe = 0.0
        self.boilKettleTimeSetPoint = 0.0
        self.boilKettleTimeProbe = 0.0

        self.mash = []
        self.mashAdjuncts = []
        self.boilAdjuncts = []
        self.boil = {}

        self.currentStep = {
            'number': -1,
            'name': 'mash'
        }

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
        
        mashSteps = recipe["beer_json"]["RECIPES"]["RECIPE"]["MASH"]["MASH_STEPS"]["MASH_STEP"]
        for step in mashSteps:
            self.mash.append({
                'state': 'Pending',
                'type': step['TYPE'],
                'decoction_amount': float("{0:.2f}".format(float(step['DECOCTION_AMT'].split(" ")[0]))),
                'infuse_amount': float("{0:.2f}".format(float(step['INFUSE_AMOUNT']))),
                'infuse_temp': float("{0:.2f}".format(float(step['INFUSE_TEMP'].split(" ")[0]))),
                'step_time': float("{0:.2f}".format(float(step['STEP_TIME']))),
                'step_temp': float("{0:.2f}".format(float(step['STEP_TEMP'])))
            })

        hopAdjuncts = recipe["beer_json"]["RECIPES"]["RECIPE"]["HOPS"]["HOP"]
        hopAdjuncts += recipe["beer_json"]["RECIPES"]["RECIPE"]["MISCS"]["MISC"]
        hopAdjuncts = sorted(hopAdjuncts, key = lambda i: float(i['TIME']), reverse=True)
        for step in hopAdjuncts:
            if step['USE'] == 'Mash' or step['USE'] == 'First Wort':
                self.mashAdjuncts.append({
                    'state': 'Pending',
                    'name': step['NAME'],
                    'time': float("{0:.2f}".format(float(step['TIME']))),
                    'amount': float("{0:.5f}".format(float(step['AMOUNT'])))
                })
            elif step['USE'] == 'Boil' or step['USE'] == 'Aroma':
                self.boilAdjuncts.append({
                    'state': 'Pending',
                    'name': step['NAME'],
                    'time': float("{0:.2f}".format(float(step['TIME']))),
                    'amount': float("{0:.5f}".format(float(step['AMOUNT'])))
                })

        self.boil =  {
            'state': 'Pending',
            'step_time': float("{0:.2f}".format(float(recipe["beer_json"]["RECIPES"]["RECIPE"]["BOIL_TIME"]))),
            'step_temp': self.config.getfloat('DEFAULT', 'BOIL_TEMPERATURE')
        }

        self.cool =  {
            'state': 'Pending',
            'step_time': self.config.getfloat('DEFAULT', 'COOL_TIME'),
            'step_temp': self.config.getfloat('DEFAULT', 'COOL_TEMPERATURE')
        }




    def timerProcess(self):
        if self.currentStep['name'] == 'mash':
            if self.mashTunTimeProbe > 0:
                self.mashTunTimeProbe -= 1/60
            else:
                self.mashTunTimeProbe = 0
                self.app.jobs.remove_job('timerProcess')
                self.mash[self.currentStep['number']]['state'] = 'Finished'
                self.setNextStep()
        elif self.currentStep['name'] == 'boil':
            if self.boilKettleTimeProbe > 0:
                self.boilKettleTimeProbe -= 1/60
            else:
                self.boilKettleTimeProbe = 0
                self.app.jobs.remove_job('timerProcess')
                self.boil['state'] = 'Finished'
                self.currentStep['number'] = -1
                self.currentStep['name'] = 'cool'
                self.setNextStep()
        elif self.currentStep['name'] == 'cool':
            if self.boilKettleTimeProbe > 0:
                self.boilKettleTimeProbe -= 1/60
            if self.app.boilKettle.getTemperature() < self.cool['step_temp'] or self.boilKettleTimeProbe <= 0:
                self.app.pump.moveWater(action=waterActionsEnum.FINISHED)
                self.app.jobs.remove_job('timerProcess')
                self.cool['state'] = 'Finished'
                self.currentStep['number'] = -1
                self.currentStep['name'] = 'finish'
                self.setNextStep()



    def timerPump(self):
        
        if self.currentStep['name'] == 'mash':
            step = self.mash[self.currentStep['number']]
            if step['type'] == 'Infusion':
                if self.app.pump.getStatus() == waterActionsEnum.FINISHED and self.app.mashTun.getTemperature() >= step['step_temp']:
                    self.app.jobs.remove_job('timerPump')
                    self.app.jobs.add_job(self.timerProcess, 'interval', seconds=1, id='timerProcess', replace_existing=True)



    def timerHeating(self):
        if self.currentStep['name'] == 'mash':
            step = self.mash[self.currentStep['number']]
            if step['type'] == 'Infusion':
                if self.app.boilKettle.getTemperature() >= step['infuse_temp']:
                    self.app.jobs.remove_job('timerHeating')
                    self.app.boilKettle.stopHeating()
                    self.app.pump.moveWater(action=waterActionsEnum.KETTLE_TO_MASHTUN)
                    self.app.mashTun.heatToTemperature(step['step_temp'])
                    self.app.jobs.add_job(self.timerPump, 'interval', seconds=1, id='timerPump', replace_existing=True)
            if step['type'] == 'Temperature':
                if self.app.mashTun.getTemperature() >= step['step_temp']:
                    self.app.jobs.remove_job('timerHeating')
                    self.app.jobs.add_job(self.timerProcess, 'interval', seconds=1, id='timerProcess', replace_existing=True)
        elif self.currentStep['name'] == 'boil':
            if self.app.boilKettle.getTemperature() >= self.boil['step_temp'] and self.app.pump.getStatus() == waterActionsEnum.FINISHED:
                self.app.jobs.remove_job('timerHeating')
                self.app.jobs.add_job(self.timerProcess, 'interval', seconds=1, id='timerProcess', replace_existing=True)



    def setNextStep(self):
        self.currentStep['number'] += 1
        if self.currentStep['name'] == 'mash':
            if self.currentStep['number'] < len(self.mash):
                step = self.mash[self.currentStep['number']]

                if step['type'] == 'Infusion' and step['infuse_amount'] > 0:
                    self.app.pump.moveWater(action=waterActionsEnum.WATER_IN_FILTERED, ammount=step['infuse_amount'])
                    self.app.boilKettle.heatToTemperature(step['infuse_temp'])
                    self.app.jobs.add_job(self.timerHeating, 'interval', seconds=1, id='timerHeating', replace_existing=True)
        
                elif step['type'] == 'Temperature':
                    self.app.mashTun.heatToTemperature(step['step_temp'])
                    self.app.jobs.add_job(self.timerHeating, 'interval', seconds=1, id='timerHeating', replace_existing=True)

                elif step['type'] == 'Decoction':
                    # TODO: handle the decoction process
                    self.setNextStep()

                self.mashTunTimeSetPoint = step['step_time']
                self.mashTunTimeProbe = step['step_time']
                self.mash[self.currentStep['number']]['state'] = 'Running'
                print('[STEP-MASH: '+str(self.currentStep['number'])+']', json.dumps(self.mash[self.currentStep['number']], indent=2))

            else:
                # start boil process
                self.currentStep['number'] = -1
                self.currentStep['name'] = 'boil'
                self.setNextStep()

        elif self.currentStep['name'] == 'boil':
            step = self.boil
            self.boilKettleTimeSetPoint = step['step_time']
            self.boilKettleTimeProbe = step['step_time']
            self.boil['state'] = 'Running'
            self.app.mashTun.stopHeating()
            self.app.pump.moveWater(action=waterActionsEnum.MASHTUN_TO_KETTLE)
            self.app.boilKettle.heatToTemperature(step['step_temp'])
            self.app.jobs.add_job(self.timerHeating, 'interval', seconds=1, id='timerHeating', replace_existing=True)
            print('[BOIL]', json.dumps(self.boil, indent=2))

        elif self.currentStep['name'] == 'cool':
            step = self.cool
            self.boilKettleTimeSetPoint = 0
            self.cool['state'] = 'Running'
            self.boilKettleTimeSetPoint = step['step_time']
            self.boilKettleTimeProbe = step['step_time']
            self.app.boilKettle.setTemperature(0)
            self.app.pump.moveWater(action=waterActionsEnum.CHILL)
            self.app.jobs.add_job(self.timerProcess, 'interval', seconds=1, id='timerProcess', replace_existing=True)
            print('[COOL]', json.dumps(self.cool, indent=2))

        elif self.currentStep['name'] == 'finish':
            self.initialize()
            self.app.ws.setLog({
                self.config.get('DEFAULT', 'LOG_NOTICE_LABEL'): 
                'The cooking process has finished!. Please dump the wort manually.'
            })




    def start(self, recipeId):
        self.initialize()
        self.loadRecipe(recipeId)
        self.setNextStep()
