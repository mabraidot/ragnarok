from subprocess import call

class Power:
    def __init__(self, app):
        self.app = app
    
    def setOff(self):
        call("sudo halt", shell=True)
