from RPi import GPIO
from time import sleep
import datetime
import threading
from app.lib.sourcesEnum import soundsEnum
import pygame

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
        pygame.mixer.init()


    def playWelcome(self):
        pygame.mixer.music.load("app/sounds/welcome.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(1000)
        self.stopSounds = True


    def playAlarm(self):
        while not self.stopSounds:
            self.buzzerState = not self.buzzerState
            if self.buzzerState:
                self.buzzerDevice.ChangeFrequency(1000)
            else:
                self.buzzerDevice.ChangeFrequency(400)
            sleep(0.7)


    def play(self, tune, duration=0):
        if self.stopSounds and not self.config.getboolean('DEFAULT', 'SILENT'):
            if tune == soundsEnum.WELCOME:
                self.stopSounds = False
                self.task = threading.Thread(target=self.playWelcome)
                self.task.start()
            elif tune == soundsEnum.ALARM:
                self.stopSounds = False
                # self.buzzerDevice.start(50)
                # self.task = threading.Thread(target=self.playAlarm)
                # self.task.start()

            if duration > 0:
                self.app.jobs.add_job(
                    self.stop, 
                    'date', 
                    run_date=datetime.datetime.now() + datetime.timedelta(seconds=duration), 
                    id='timerSound', 
                    replace_existing=True)


    def stop(self):
        self.stopSounds = True
        # self.buzzerDevice.stop()