from app.hardware.sourcesEnum import sourcesEnum

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

    def moveWater(self, moveFrom, moveTo):
        if not isinstance(moveFrom, sourcesEnum):
            raise TypeError("%s attribute must be set to an instance of %s" % (moveFrom, sourcesEnum))
        if not isinstance(moveTo, sourcesEnum):
            raise TypeError("%s attribute must be set to an instance of %s" % (moveTo, sourcesEnum))

        # if moveFrom == sourcesEnum.INLET_FILTERED:
            # open 