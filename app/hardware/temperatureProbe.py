import threading
import time

class temperatureProbe:
    def __init__(self, app, config, name = 'MashTunTemperatureProbe'):
        self.app = app
        self.config = config
        self.name = name
        self.value = 0


        if self.config.get('ENVIRONMENT') == 'production':
            # https://github.com/thegreathoe/cbpi-pt100-sensor
            from app.lib import max31865
            if self.config.getint('TEMPERATURE_SENSOR_SPI_PORT') == 1:
                cs = 22
            else:
                cs = 27

            self.sensor = max31865.max31865(int(cs), 9, 10, 11, 430, int(0xD2))

            task = threading.Thread(target=self.run)
            task.start()



    def get(self):
        if self.config.get('ENVIRONMENT') == 'development':
            # TODO: this is a TEST. Return the actual value
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
        while True:
            # oldValue = self.value
            newValue = self.sensor.readTemp()
            # if abs(oldValue - newValue) < 50:
            self.value = newValue
            time.sleep(0.5)