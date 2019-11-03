from aiohttp import web
from app.routes import routes
from app.webSocket import webSocket
from app.sensors.temperatureProbe import temperatureProbe

app = web.Application()
app.ws = webSocket(app)

# Hardware
app.mashTunTempProbe = temperatureProbe(app, 'MashTunTemperatureProbe')

# API routes definition
r = routes(app)
r.setup_routes()

# Jobs scheduler
# app.mashTunTempProbe.sendToWebSocket()

if __name__ == '__main__':
    web.run_app(app)
