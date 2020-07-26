from time import sleep
import datetime
import threading
from app.lib.sourcesEnum import soundsEnum
import pygame

class Sound:
    def __init__(self, app, config):
        self.app = app
        self.config = config
        self.buzzerState = False
        self.stopSounds = True
        self.task=0
        pygame.mixer.init()


    def playWelcome(self):
        pygame.mixer.music.load("app/sounds/welcome.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(1000)
        self.stopSounds = True


    def playGoodbye(self):
        pygame.mixer.music.load("app/sounds/goodbye.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(1000)
        self.stopSounds = True


    def playSuccess(self):
        pygame.mixer.music.load("app/sounds/success.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(1000)
        self.stopSounds = True


    def playAlarm(self):
        while not self.stopSounds:
            pygame.mixer.music.load("app/sounds/alarm.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.wait(1000)


    def play(self, tune, duration=0):
        if self.stopSounds and not self.config.getboolean('DEFAULT', 'SILENT'):
            if tune == soundsEnum.WELCOME:
                self.stopSounds = False
                self.task = threading.Thread(target=self.playWelcome)
                self.task.start()
            elif tune == soundsEnum.GOODBYE:
                self.stopSounds = False
                self.task = threading.Thread(target=self.playGoodbye)
                self.task.start()
            elif tune == soundsEnum.ALARM:
                self.stopSounds = False
                self.task = threading.Thread(target=self.playAlarm)
                self.task.start()
            elif tune == soundsEnum.SUCCESS:
                self.stopSounds = False
                self.task = threading.Thread(target=self.playSuccess)
                self.task.start()

            if duration > 0:
                self.app.jobs.add_job(
                    self.stop, 
                    'date', 
                    run_date=datetime.datetime.now() + datetime.timedelta(seconds=duration), 
                    id='timerSound', 
                    replace_existing=True)


    def stop(self):
        self.stopSounds = True