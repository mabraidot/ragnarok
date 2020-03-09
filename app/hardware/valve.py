class valve:
    def __init__(self, app, config, channel, name):
        self.app = app
        self.config = config
        self.name = name
        self.value = 0
        self.channel = channel
    
    def get(self):
        return self.value
    
    def set(self, newValue = 0):
        self.value = int(newValue)
        if self.config.get('DEFAULT', 'ENVIRONMENT') == 'production':
            # newValue: percentage, 100 % = 63 servo degrees
            self.app.servoKit.servo[self.channel].angle(int(self.value * 0.63))
