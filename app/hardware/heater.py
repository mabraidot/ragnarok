class heater:
    def __init__(self, app, pin, name = 'MashTunHeater'):
        self.app = app
        self.name = name
        self.pin = pin
        self.value = False
        self.pwm = 0
    
    def get(self):
        return self.value
    
    def set(self, newState = 'false'):
        if newState == 'true':
            self.value = True
        else:
            self.value = False

    def pid(self, tempSetPoint, currentTemp):
        # TODO: implement actual PID logic. Just for testing
        if(currentTemp >= tempSetPoint):
            self.set('false')
        else:
            self.set('true')