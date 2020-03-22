import threading
import time
# import busio
# import digitalio
# import adafruit_max31865
import statistics

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

            # https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/
            # https://learn.adafruit.com/adafruit-max31865-rtd-pt100-amplifier/python-circuitpython
            # import board
            # spi = busio.SPI(
            #     board.SCK, 
            #     board.MOSI, 
            #     board.MISO)
            # if self.config.getint('TEMPERATURE_SENSOR_SPI_PORT') == 1:
            #     cs = digitalio.DigitalInOut(board.D22)
            # else:
            #     cs = digitalio.DigitalInOut(board.D27)

            # self.sensor = adafruit_max31865.MAX31865(spi, cs, rtd_nominal=100, ref_resistor=430.0, wires=3)

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
        valueList = []
        while True:
            valueList.append(self.sensor.readTemp())
            if len(valueList) > 5:
                self.value = statistics.median(valueList)
                valueList = []
            time.sleep(0.2)
            # print('---->', valueList, self.value)
            # oldValue = self.value
            # # newValue = self.sensor.temperature
            # newValue = self.sensor.readTemp()
            # if abs(oldValue - newValue) < 50:
            #     self.value = newValue
            # time.sleep(1)