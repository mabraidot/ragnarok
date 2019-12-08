class valve:
    def __init__(self, app, name):
        self.app = app
        self.name = name
        self.value = 0
    
    def get(self):
        return self.value
    
    def set(self, newValue = 0):
        self.value = newValue
