
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
adjunts = [{
    state: ('Pending', 'Running', 'Finished'),
    use: ('Mash', 'First Wort', 'Boil', 'Dry Hop', 'Aroma', 'Primary', 'Secondary' or 'Bottling'),
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
        self.adjunts = []
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
        print(recipe["name"])