from RPi import GPIO

class valve:
    def __init__(self, app, config, channel, name):
        self.app = app
        self.config = config
        self.name = name
        self.value = 0
        self.channel = channel
        self.enablePin = self.config.getint('GENERAL_PINS', 'SERVO_ENABLE')
        GPIO.setmode(GPIO.BCM)
        # GPIO.setup(self.enablePin, GPIO.OUT)
        GPIO.setwarnings(False)
        # GPIO.output(self.enablePin, GPIO.HIGH)
    
    def get(self):
        return self.value
    
    def set(self, newValue = 0):
        self.value = int(newValue)
        if self.config.get('DEFAULT', 'ENVIRONMENT') == 'production':
            # newValue: percentage, 100 % = 90 servo degrees
            GPIO.output(self.enablePin, GPIO.LOW)
            self.app.servoKit.servo[self.channel].angle = int(self.value * 0.90)
            GPIO.output(self.enablePin, GPIO.HIGH)