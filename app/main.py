from aiohttp import web
from app.routes import routes
from app.webSocket import webSocket
from app.cooking import Cooking
from app.hardware.kettle import kettle
from app.hardware.valve import valve
from app.hardware.pump import pump
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database import Database
from app.recipes import Recipes
import configparser

config = configparser.ConfigParser()
config.read('app/config/config.cfg')

app = web.Application()
app.recipes = Recipes(app)
app.DB = Database(app, config)

# Jobs scheduler
app.jobs = AsyncIOScheduler()
app.jobs.start()

# Main cooking process
app.cooking = Cooking(app)

# Hardware
app.mashTun = kettle(app, config['MASH_TUN_PINS'], 'MashTun')
app.boilKettle = kettle(app, config['BOIL_KETTLE_PINS'], 'BoilKettle')

app.pump = pump(app, 'Pump')

app.outletValveDump = valve(app, 'OutletValveDump')
app.chillerValveWort = valve(app, 'ChillerValveWort')
app.chillerValveWater = valve(app, 'ChillerValveWater')
app.boilKettleValveOutlet = valve(app, 'BoilKettleValveOutlet')
app.boilKettleValveInlet = valve(app, 'BoilKettleValveInlet')
app.boilKettleValveWater = valve(app, 'BoilKettleValveWater')
app.mashTunValveOutlet = valve(app, 'MashTunValveOutlet')
app.mashTunValveInlet = valve(app, 'MashTunValveInlet')

# Start websocket server
app.ws = webSocket(app)

# API routes definition
r = routes(app, config)
r.setup_routes()

if __name__ == '__main__':
    web.run_app(app)
