import json

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
    time: 0
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
    def __init__(self, app):
        self.app = app
        self.mashTunTimeSetPoint = 0
        self.mashTunTimeProbe = 0
        self.boilKettleTimeSetPoint = 0
        self.boilKettleTimeProbe = 0

        self.mash = []
        self.mashAdjuncts = []
        self.boilAdjuncts = []
        self.boil = {}


    def getMashTunTimeSetPoint(self):
        return self.mashTunTimeSetPoint


    def getMashTunTimeProbe(self):
        return self.mashTunTimeProbe


    def getBoilKettleTimeSetPoint(self):
        return self.boilKettleTimeSetPoint


    def getBoilKettleTimeProbe(self):
        return self.boilKettleTimeProbe


    def start(self, recipeId):
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
            'time': float("{0:.2f}".format(float(recipe["beer_json"]["RECIPES"]["RECIPE"]["BOIL_TIME"])))
        }

        print(json.dumps(self.boil, indent=2))