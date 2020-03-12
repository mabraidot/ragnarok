from subprocess import call
from app.lib.sourcesEnum import soundsEnum
import time

class Power:
    def __init__(self, app):
        self.app = app
    
    def setOff(self):
        self.app.sound.play(soundsEnum.GOODBYE)
        time.sleep(1.5)
        call("sudo halt", shell=True)
