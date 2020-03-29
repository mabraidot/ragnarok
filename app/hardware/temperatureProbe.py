import threading
import time

class temperatureProbe:
    def __init__(self, app, config, name = 'MashTunTemperatureProbe'):
        self.app = app
        self.config = config
        self.name = name
        self.value = 0
        self.sensor = None

        if self.config.get('ENVIRONMENT') == 'production':
            # from w1thermsensor import W1ThermSensor
            # self.sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, self.config.get('TEMPERATURE_SENSOR_ADDRESS'))
            self.initSensor()


    def initSensor(self):
        if self.config.get('ENVIRONMENT') == 'production':
            from w1thermsensor import W1ThermSensor
            self.sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, self.config.get('TEMPERATURE_SENSOR_ADDRESS'))
            task = threading.Thread(target=self.run)
            task.start()


    def get(self):
        if self.config.get('ENVIRONMENT') == 'development':
            heater = self.app.mashTun.getHeater()
            pwm = self.app.mashTun.getPWM()
            if self.name == 'BoilKettleTemperatureProbe':
                heater = self.app.boilKettle.getHeater()
                pwm = self.app.boilKettle.getPWM()
            if heater and pwm > 0 and self.value < 110:
                self.value += 1 * (pwm / 100)
            elif self.value > 0:
                self.value -= 0.1

        return self.value + self.config.getint('TEMPERATURE_SENSOR_OFFSET')


    def run(self):
        try:
            while True:
                # oldValue = self.value
                newValue = self.sensor.get_temperature()
                # if abs(oldValue - newValue) < 50:
                self.value = newValue
                time.sleep(0.5)
        except:
            self.initSensor()