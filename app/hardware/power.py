from subprocess import call
from app.lib.sourcesEnum import soundsEnum
import time

class Power:
    def __init__(self, app):
        self.app = app
    
    def setOff(self):
        self.app.sound.play(soundsEnum.GOODBYE)
        time.sleep(3)
        call("sudo halt", shell=True)
