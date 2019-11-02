import random
from aiohttp import web

def setup_routes(app):
    app.add_routes([
        web.get('/', home),
        web.get('/index', home),
        web.get('/mashtun', getMashTunTemperature),
        web.get('/mashtun/get/temperature', getMashTunTemperature),
        web.get('/mashtun/set/temperature/{degrees}', setMashTunTemperature)
    ])


def home(request):
    return web.json_response({'response': 'The Ragnarök is coming ...'})


def getMashTunTemperature(request):
    return web.json_response({'temperature': random.randrange(0, 100)})


def setMashTunTemperature(request):
    degrees = request.match_info.get('degrees', 0)
    return web.json_response({'response': str(degrees)})