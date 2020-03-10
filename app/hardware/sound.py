from RPi import GPIO
from time import sleep
import datetime
import threading
from app.lib.sourcesEnum import soundsEnum

class Sound:
    def __init__(self, app, config):
        self.app = app
        self.config = config
        self.buzzerPin = self.config.getint('GENERAL_PINS', 'BUZZER')
        self.buzzerState = False
        self.stopSounds = True
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.buzzerPin, GPIO.OUT)
        self.task=0
        self.buzzerDevice = GPIO.PWM(self.buzzerPin, 440)


    def playAlarm(self):
        while not self.stopSounds:
            self.buzzerState = not self.buzzerState
            if self.buzzerState:
                self.buzzerDevice.ChangeFrequency(1000)
            else:
                self.buzzerDevice.ChangeFrequency(400)
            sleep(0.7)


    def play(self, tune, duration=10):
        if self.stopSounds:
            if tune == soundsEnum.ALARM:
                self.stopSounds = False
                self.buzzerDevice.start(50)
                self.task = threading.Thread(target=self.playAlarm)
                self.task.start()
                self.app.jobs.add_job(
                    self.stop, 
                    'date', 
                    run_date=datetime.datetime.now() + datetime.timedelta(seconds=duration), 
                    id='timerSound', 
                    replace_existing=True)


    def stop(self):
        self.stopSounds = True
        self.buzzerDevice.stop()