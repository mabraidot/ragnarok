from aiohttp import web
from app.routes import routes
from app.webSocket import webSocket
from app.cooking import Cooking
from app.hardware.kettle import kettle
from app.hardware.valve import valve
from apscheduler.schedulers.asyncio import AsyncIOScheduler

app = web.Application()
app.ws = webSocket(app)

# Jobs scheduler
app.jobs = AsyncIOScheduler()
app.jobs.start()

# Main cooking process
app.cooking = Cooking(app)

# Hardware
app.mashTun = kettle(app, 'MashTun')
app.boilKettle = kettle(app, 'BoilKettle')

app.outletValveDump = valve(app, 'OutletValveDump')
app.chillerValveWort = valve(app, 'ChillerValveWort')
app.chillerValveWater = valve(app, 'ChillerValveWater')
app.boilKettleValveOutlet = valve(app, 'BoilKettleValveOutlet')
app.boilKettleValveInlet = valve(app, 'BoilKettleValveInlet')
app.boilKettleValveWater = valve(app, 'BoilKettleValveWater')
app.mashTunValveOutlet = valve(app, 'MashTunValveOutlet')
app.mashTunValveInlet = valve(app, 'MashTunValveInlet')

# API routes definition
r = routes(app)
r.setup_routes()

if __name__ == '__main__':
    web.run_app(app)
