import random
from aiohttp import web

class routes:
    def __init__(self, app):
        self.app = app

    def setup_routes(self):
        self.app.add_routes([
            web.get('/', self.home),
            web.get('/index', self.home),
            web.get('/mashtun', self.getMashTunTemperature),
            web.get('/mashtun/get/temperature', self.getMashTunTemperature),
            web.get('/mashtun/set/temperature/{degrees}', self.setMashTunTemperature)
        ])


    def home(self, request):
        return web.json_response({'response': 'The Ragnarök is coming ...'})


    def getMashTunTemperature(self, request):
        return web.json_response({'temperature': random.randrange(0, 100)})


    def setMashTunTemperature(self, request):
        degrees = request.match_info.get('degrees', 0)
        return web.json_response({'response': str(degrees)})