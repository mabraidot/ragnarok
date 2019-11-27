from aiohttp import web
from app.routes import routes
from app.webSocket import webSocket
from app.cooking import Cooking
from app.hardware.kettle import kettle
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

# API routes definition
r = routes(app)
r.setup_routes()

if __name__ == '__main__':
    web.run_app(app)
