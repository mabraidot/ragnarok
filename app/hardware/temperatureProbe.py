import threading
import time
# import board
import busio
import digitalio
import adafruit_max31865

class temperatureProbe:
    def __init__(self, app, config, name = 'MashTunTemperatureProbe'):
        self.app = app
        self.config = config
        self.name = name
        self.value = 0

        # https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/
        # https://learn.adafruit.com/adafruit-max31865-rtd-pt100-amplifier/python-circuitpython

        if self.config.get('ENVIRONMENT') == 'production':
            import board
            # TODO: enable this on the actual raspberry because a platform error on windows
            if self.config.getint('TEMPERATURE_SENSOR_SPI_PORT') == 1:
                spi = busio.SPI(
                    board.SCK, 
                    board.MOSI, 
                    board.MISO)
                cs = digitalio.DigitalInOut(board.D8)
            else:
                spi = busio.SPI(
                    board.SCK_1, 
                    board.MOSI_1, 
                    board.MISO_1)
                cs = digitalio.DigitalInOut(board.D18)

            self.sensor = adafruit_max31865.MAX31865(spi, cs, rtd_nominal=100, ref_resistor=430.0, wires=3)

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

        return self.value


    def run(self):
        while True:
            oldValue = self.value
            newValue = self.sensor.temperature
            if abs(oldValue - newValue) < 50:
                self.value = newValue
            time.sleep(1)