from aiohttp import web
from app.routes import routes
from app.webSocket import webSocket
from app.sensors.temperatureProbe import temperatureProbe
from apscheduler.schedulers.asyncio import AsyncIOScheduler

app = web.Application()
app.ws = webSocket(app)

# Hardware
app.mashTunTempProbe = temperatureProbe(app, 'MashTunTemperatureProbe')

# API routes definition
r = routes(app)
r.setup_routes()

# Jobs scheduler
jobs = AsyncIOScheduler()
jobs.start()
jobs.add_job(app.mashTunTempProbe.sendToWebSocket, 'interval', seconds=1)

if __name__ == '__main__':
    web.run_app(app)
