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
        self.task = 0
        self.siblingHeater = None
        

    def get(self):
        return self.value


    def set(self, newState = 'false'):
        if self.name == 'MashTunHeater':
            self.siblingHeater = self.app.boilKettle.heater
        else:
            self.siblingHeater = self.app.mashTun.heater

        if newState == 'true':
            if not self.value:
                self.value = True
                self.task = threading.Thread(target=self.run)
                self.task.start()
        else:
            self.value = False
            self.pid(0, self.currentTemp)
            self.setPWM(0)


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
            if not self.app.mashTun.PIDAutoTune.running and not self.app.boilKettle.PIDAutoTune.running:
                self.pwm = self.pidControl(self.currentTemp)
            # print('PWM:', self.name, self.pwm)
            # print('-------------------->PWM:', min((100 - self.siblingHeater.getPWM()), self.pwm))
            # Not allowed both heaters turned on at full power
            self.pwm = min((100 - self.siblingHeater.getPWM()), self.pwm)
            self.heatDevice.ChangeDutyCycle(self.pwm)
            sleep(0.5)
        self.heatDevice.stop()
