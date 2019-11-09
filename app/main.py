from aiohttp import web
from app.routes import routes
from app.webSocket import webSocket
from app.hardware.temperatureProbe import temperatureProbe
from apscheduler.schedulers.asyncio import AsyncIOScheduler

app = web.Application()
app.ws = webSocket(app)

# Jobs scheduler
app.jobs = AsyncIOScheduler()
app.jobs.start()

# Hardware
app.mashTunTempProbe = temperatureProbe(app, 'MashTunTemperatureProbe')
app.boilKettleTempProbe = temperatureProbe(app, 'BoilKettleTemperatureProbe')

# API routes definition
r = routes(app)
r.setup_routes()

if __name__ == '__main__':
    web.run_app(app)
