from aiohttp import web
from app.routes import routes
from app.webSocket import webSocket
from app.cooking import Cooking
from app.hardware.temperatureProbe import temperatureProbe
from app.hardware.waterLevelProbe import waterLevelProbe
from app.hardware.heater import heater
from apscheduler.schedulers.asyncio import AsyncIOScheduler

app = web.Application()
app.ws = webSocket(app)

# Jobs scheduler
app.jobs = AsyncIOScheduler()
app.jobs.start()

# Main cooking process
app.cooking = Cooking(app)

# Hardware
app.mashTunTempProbe = temperatureProbe(app, 'MashTunTemperatureProbe')
app.boilKettleTempProbe = temperatureProbe(app, 'BoilKettleTemperatureProbe')
app.mashTunWaterLevelProbe = waterLevelProbe(app, 'MashTunWaterLevelProbe')
app.boilKettleWaterLevelProbe = waterLevelProbe(app, 'BoilKettleWaterLevelProbe')
app.mashTunHeater = heater(app, 'MashTunHeater')
app.boilKettleHeater = heater(app, 'BoilKettleHeater')

# API routes definition
r = routes(app)
r.setup_routes()

if __name__ == '__main__':
    web.run_app(app)
