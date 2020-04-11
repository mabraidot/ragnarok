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
            if self.config.getint('TEMPERATURE_SENSOR_SPI_PORT') == 1:
                self.initSensorMax31865()
            else:
                self.initSensorDS18B20()


    def initSensorDS18B20(self):
        if self.config.get('ENVIRONMENT') == 'production':
            from w1thermsensor import W1ThermSensor
            self.sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, self.config.get('TEMPERATURE_SENSOR_ADDRESS'))
            task = threading.Thread(target=self.runDS18B20)
            task.start()

    def initSensorMax31865(self):
        if self.config.get('ENVIRONMENT') == 'production':
            from app.lib import max31865
            self.sensor = max31865.max31865(self.config.getint('TEMPERATURE_SENSOR_ADDRESS'), 9, 10, 11, 430, int(0xD2))

            task = threading.Thread(target=self.runMax31865)
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

        currentTemperature = self.value + self.config.getint('TEMPERATURE_SENSOR_OFFSET')
        if (currentTemperature > 25 
            and self.config.get('ENVIRONMENT') == 'production' 
            and self.config.getint('TEMPERATURE_SENSOR_SPI_PORT') == 1):
            currentTemperature = ((47 / 35) * (currentTemperature - 25)) + 25
        return currentTemperature


    def runDS18B20(self):
        try:
            while True:
                # oldValue = self.value
                newValue = self.sensor.get_temperature()
                # if abs(oldValue - newValue) < 50:
                self.value = newValue
                time.sleep(0.5)
        except:
            self.initSensorDS18B20()


    def runMax31865(self):
        while True:
            # oldValue = self.value
            newValue = self.sensor.readTemp()
            # if abs(oldValue - newValue) < 50:
            self.value = newValue
            time.sleep(0.5)