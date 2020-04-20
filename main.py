from RPi import GPIO
from aiohttp import web
from app.routes import routes
from app.webSocket import webSocket
from app.cooking import Cooking
from app.hardware.kettle import kettle
from app.hardware.pump import pump
from app.hardware.sound import Sound
from app.hardware.power import Power
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from app.recipes import Recipes
import configparser
import platform
import logging
import logging.handlers


try:
    config = configparser.ConfigParser()
    config.read('app/config/config.cfg')

    app = web.Application()
    app.recipes = Recipes(app, config)
    app.sound = Sound(app, config)
    app.started = False

    # Logging
    LOG_FILENAME = 'app/logs/app.log'
    formatter = logging.Formatter('%(asctime)s;%(levelname)s;%(message)s')
    app.logger = logging.getLogger('RagnarokLogger')
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=200000, backupCount=5)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

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

    app.pump = pump(app, config, 'Pump')

    # Main cooking process
    app.cooking = Cooking(app, config)

    # Start websocket server
    app.ws = webSocket(app)

    # API routes definition
    r = routes(app, config)
    r.setup_routes()
except Exception as e:
    # app.logger.error(e)
    app.logger.exception(e)

if __name__ == '__main__':
    try:
        web.run_app(app, port=8000)
    finally:  
        print('Exiting Ragnarok ...')
        GPIO.cleanup()
