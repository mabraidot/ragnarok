from RPi.GPIO import GPIO
from time import sleep
from app.hardware.sourcesEnum import soundsEnum
import threading

class Sound:
    def __init__(self, app, config):
        self.app = app
        self.config = config
        self.buzzerTime = 1
        self.buzzerDelay = 2
        self.buzzerPin = self.config.getint('GENERAL_PINS', 'BUZZER')
        self.buzzerState = False
        self.killSounds = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buzzerPin, GPIO.OUT)

    #     self.alarm = [
    #         ('C#4', 0.2), ('D4', 0.2),  (None, 0.2),
    #         ('Eb4', 0.2), ('E4', 0.2),  (None, 0.6),
    #         ('F#4', 0.2), ('G4', 0.2),  (None, 0.6),
    #         ('Eb4', 0.2), ('E4', 0.2),  (None, 0.2),
    #         ('F#4', 0.2), ('G4', 0.2),  (None, 0.2),
    #         ('C4', 0.2),  ('B4', 0.2),  (None, 0.2),
    #         ('F#4', 0.2), ('G4', 0.2),  (None, 0.2),
    #         ('B4', 0.2),  ('Bb4', 0.5), (None, 0.6),
    #         ('A4', 0.2),  ('G4', 0.2),  ('E4', 0.2),
    #         ('D4', 0.2),  ('E4', 0.2)
    #     ]


    # def play(self, tune):
    #     for note, duration in tune:
    #         self.buzzer.play(note)
    #         sleep(float(duration))
    #     self.buzzer.stop()

    def playAlarm(self):
        while True:
            if self.killSounds:
                break
            self.buzzerState = not self.buzzerState
            GPIO.output(self.buzzerPin, self.buzzerState)
            sleep(1)


    def play(self, tune):
        if tune == soundsEnum.ALARM:
            task = threading.Thread(target=self.playAlarm)
            task.start()


    def stop(self):
        self.killSounds = True
        # if self.app.jobs.get_job('timerSound') is not None:
        #     self.app.jobs.remove_job('timerSound')
