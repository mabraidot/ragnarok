from RPi import GPIO
from simple_pid import PID
import threading
from time import sleep

class heater:
    def __init__(self, app, config, name = 'MashTunHeater'):
        self.app = app
        self.name = name
        self.config = config
        self.pin = self.config.getint('HEATER')
        self.value = False
        self.pwm = 0
        self.setPoint = 0
        self.currentTemp = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.setwarnings(False)
        self.heatDevice = GPIO.PWM(self.pin, 100)
        self.pidControl = PID(
            self.config.getfloat('PID_KP'), 
            self.config.getfloat('PID_KI'), 
            self.config.getfloat('PID_KD'), 
            setpoint=0)
        self.pidControl.sample_time = 1
        self.pidControl.output_limits = (0, 100)
        self.pidControl.auto_mode = True


    def get(self):
        return self.value


    def set(self, newState = 'false'):
        if newState == 'true':
            self.value = True
            task = threading.Thread(target=self.run)
            task.start()
        else:
            self.value = False


    def setPWM(self, newPWM = 0):
        self.pwm = int(newPWM)


    def getPWM(self):
        return self.pwm


    def pid(self, tempSetPoint, currentTemp):
        self.setPoint = float(tempSetPoint)
        self.currentTemp = float(currentTemp)
        self.pidControl.setpoint = self.setPoint


    def run(self):
        self.heatDevice.start(0)
        while self.value:
            self.pwm = self.pidControl(self.currentTemp)
            self.heatDevice.ChangeDutyCycle(self.pwm)
            sleep(0.5)
        self.heatDevice.stop()
        GPIO.cleanup()