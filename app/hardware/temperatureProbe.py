from RPi import GPIO
import threading
import time
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

        # Enabling Second SPI
        # If you are using the main SPI port for a display or something and need another hardware SPI port, you can enable it by adding the line
        # dtoverlay=spi1-3cs
        # to the bottom of /boot/config.txt and rebooting. You'll then see the addition of some /dev/spidev1.x devices:
        # $ ls /dev/spi*

        # TODO: enable this on the actual raspberry because a platform error on windows
        spi = busio.SPI(
            self.config.getint('TEMPERATURE_SENSOR_SCLK'), 
            self.config.getint('TEMPERATURE_SENSOR_MOSI'), 
            self.config.getint('TEMPERATURE_SENSOR_MISO'))
        cs = digitalio.DigitalInOut(self.config.getint('TEMPERATURE_SENSOR_CS'))  # Chip select of the MAX31865 board.
        self.sensor = adafruit_max31865.MAX31865(spi, cs, rtd_nominal=100, ref_resistor=430.0, wires=3)

        task = threading.Thread(target=self.run)
        task.start()



    def get(self):
        # TODO: this is a TEST. Return the actual value
        # heater = self.app.mashTun.getHeater()
        # pwm = self.app.mashTun.getPWM()
        # if self.name == 'BoilKettleTemperatureProbe':
        #     heater = self.app.boilKettle.getHeater()
        #     pwm = self.app.boilKettle.getPWM()
        # if heater and pwm > 0 and self.value < 110:
        #     self.value += 1 * (pwm / 100)
        # elif self.value > 0:
        #     self.value -= 0.1

        return self.value


    def run(self):
        try:
            while True:
                self.value = self.sensor.temperature
                time.sleep(1)
        except:
            GPIO.cleanup()