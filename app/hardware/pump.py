class pump:
    def __init__(self, app, name):
        self.app = app
        self.name = name
        self.value = False
    
    def get(self):
        return self.value
    
    def set(self, newState = 'false'):
        if newState == 'true':
            self.value = True
        else:
            self.value = False

    def moveWater(self, moveFrom, moveTo, quantity):
        """
        Sources:
        -------
        INLET_FILTERED
        INLET
        MASHTUN
        BOILKETTLE
        CHILLER_WORT
        CHILLER_WATER (to dump)
        OUTLET
        """