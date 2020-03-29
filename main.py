from RPi import GPIO
from aiohttp import web
from app.routes import routes
from app.webSocket import webSocket
from app.cooking import Cooking
from app.hardware.kettle import kettle
# from app.hardware.valve import valve
from app.hardware.pump import pump
from app.hardware.sound import Sound
from app.hardware.power import Power
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from app.recipes import Recipes
import configparser
import platform
# from app.lib.sourcesEnum import soundsEnum

config = configparser.ConfigParser()
config.read('app/config/config.cfg')

app = web.Application()
app.recipes = Recipes(app, config)
app.sound = Sound(app, config)
app.started = False

# Jobs scheduler
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': True,
    'max_instances': 3
}
app.jobs = AsyncIOScheduler(executors=executors, job_defaults=job_defaults)
app.jobs.start()

# Hardware
app.power = Power(app)
app.mashTun = kettle(app, config['MASH_TUN_PINS'], 'MashTun')
app.boilKettle = kettle(app, config['BOIL_KETTLE_PINS'], 'BoilKettle')
# if config.get('DEFAULT', 'ENVIRONMENT') == 'production':
#     from adafruit_servokit import ServoKit
#     from RPi import GPIO
#     app.servoKit = ServoKit(channels=8)
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(config.getint('GENERAL_PINS','SERVO_ENABLE'), GPIO.OUT)
#     GPIO.setwarnings(False)
#     GPIO.output(config.getint('GENERAL_PINS','SERVO_ENABLE'), GPIO.HIGH)

app.pump = pump(app, config, 'Pump')

# Main cooking process
app.cooking = Cooking(app, config)

# app.outletValveDump = valve(app, config, 0, 'OutletValveDump')
# app.chillerValveWort = valve(app, config, 1, 'ChillerValveWort')
# app.chillerValveWater = valve(app, config, 2, 'ChillerValveWater')
# app.boilKettleValveOutlet = valve(app, config, 3, 'BoilKettleValveOutlet')
# app.boilKettleValveReturn = valve(app, config, 4, 'BoilKettleValveReturn')
# app.mashTunValveOutlet = valve(app, config, 5, 'MashTunValveOutlet')
# app.mashTunValveInlet = valve(app, config, 6, 'MashTunValveInlet')
# # Valve inlet and waterin channels are shared
# app.boilKettleValveInlet = valve(app, config, 7, 'BoilKettleValveInlet')
# app.boilKettleValveWater = valve(app, config, 7, 'BoilKettleValveWater')

# Start websocket server
app.ws = webSocket(app)

# API routes definition
r = routes(app, config)
r.setup_routes()

# app.sound.play(soundsEnum.ALARM, 25)

if __name__ == '__main__':
    try:
        web.run_app(app, port=8000)
    finally:  
        print('Exiting Ragnarok ...')
        GPIO.cleanup()
