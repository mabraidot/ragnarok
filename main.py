from RPi import GPIO
from aiohttp import web
from app.routes import routes
from app.webSocket import webSocket
from app.cooking import Cooking
from app.hardware.kettle import kettle
from app.hardware.valve import valve
from app.hardware.pump import pump
from app.hardware.sound import Sound
from app.hardware.power import Power
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database import Database
from app.recipes import Recipes
import configparser
import platform
from app.lib.sourcesEnum import soundsEnum

config = configparser.ConfigParser()
config.read('app/config/config.cfg')

app = web.Application()
app.DB = Database(app, config)
app.recipes = Recipes(app)
app.sound = Sound(app, config)

# Jobs scheduler
app.jobs = AsyncIOScheduler()
app.jobs.start()

# Hardware
app.power = Power(app)
app.mashTun = kettle(app, config['MASH_TUN_PINS'], 'MashTun')
app.boilKettle = kettle(app, config['BOIL_KETTLE_PINS'], 'BoilKettle')
if config.get('DEFAULT', 'ENVIRONMENT') == 'production':
    from adafruit_servokit import ServoKit
    app.servoKit = ServoKit(channels=8)

app.pump = pump(app, config, 'Pump')

# Main cooking process
app.cooking = Cooking(app, config)

app.outletValveDump = valve(app, config, 0, 'OutletValveDump')
app.chillerValveWort = valve(app, config, 1, 'ChillerValveWort')
app.chillerValveWater = valve(app, config, 2, 'ChillerValveWater')
app.boilKettleValveOutlet = valve(app, config, 3, 'BoilKettleValveOutlet')
app.boilKettleValveReturn = valve(app, config, 4, 'BoilKettleValveReturn')
app.mashTunValveOutlet = valve(app, config, 5, 'MashTunValveOutlet')
app.mashTunValveInlet = valve(app, config, 6, 'MashTunValveInlet')
# Valve inlet and waterin channels are shared
app.boilKettleValveInlet = valve(app, config, 7, 'BoilKettleValveInlet')
app.boilKettleValveWater = valve(app, config, 7, 'BoilKettleValveWater')

# Start websocket server
app.ws = webSocket(app)

# API routes definition
r = routes(app, config)
r.setup_routes()

app.sound.play(soundsEnum.WELCOME)

if __name__ == '__main__':
    try:
        web.run_app(app, port=8000)
    finally:  
        print('Exiting Ragnarok ...')
        GPIO.cleanup()
