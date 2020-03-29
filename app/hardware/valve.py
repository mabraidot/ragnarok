from RPi import GPIO
from time import sleep
import threading

class valve:
    def __init__(self, app, config, channel, name):
        self.app = app
        self.config = config
        self.name = name
        self.value = 0
        self.channel = channel
        self.enablePin = self.config.getint('GENERAL_PINS', 'SERVO_ENABLE')
    
    def get(self):
        return self.value
    
    def set(self, newValue = 0):
        self.value = int(newValue)
        if self.config.get('DEFAULT', 'ENVIRONMENT') == 'production':
            # task = threading.Thread(target=self.run)
            # task.start()
            # newValue: percentage, 100 % = 90 servo degrees
            GPIO.output(self.enablePin, GPIO.LOW)
            sleep(0.2)
            self.app.servoKit.servo[self.channel].angle = int(self.value * 0.90)
            sleep(1)
            self.app.servoKit.servo[self.channel].angle = None
            self.app.servoKit.servo[self.channel].fraction = None
            GPIO.output(self.enablePin, GPIO.HIGH)
            sleep(0.2)
            

    def run(self):
        # newValue: percentage, 100 % = 90 servo degrees
        # GPIO.output(self.enablePin, GPIO.LOW)
        # sleep(0.2)
        self.app.servoKit.servo[self.channel].angle = int(self.value * 0.90)
        sleep(1)
        self.app.servoKit.servo[self.channel].angle = None
        self.app.servoKit.servo[self.channel].fraction = None
        # GPIO.output(self.enablePin, GPIO.HIGH)
        # sleep(0.2)