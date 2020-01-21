from RPi import GPIO
from time import sleep
import datetime
import threading
from app.hardware.sourcesEnum import soundsEnum

class Sound:
    def __init__(self, app, config):
        self.app = app
        self.config = config
        self.buzzerTime = 1
        self.buzzerDelay = 2
        self.buzzerPin = self.config.getint('GENERAL_PINS', 'BUZZER')
        self.buzzerState = False
        self.stopSounds = True
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buzzerPin, GPIO.OUT)
        GPIO.setwarnings(False)


    def playAlarm(self):
        while not self.stopSounds:
            self.buzzerState = not self.buzzerState
            GPIO.output(self.buzzerPin, self.buzzerState)
            sleep(1)
        GPIO.cleanup()


    def play(self, tune, duration=10):
        if self.stopSounds:
            if tune == soundsEnum.ALARM:
                self.stopSounds = False
                task = threading.Thread(target=self.playAlarm)
                task.start()
                self.app.jobs.add_job(
                    self.stop, 
                    'date', 
                    run_date=datetime.datetime.now() + datetime.timedelta(seconds=duration), 
                    id='timerSound', 
                    replace_existing=True)


    def stop(self):
        self.stopSounds = True