import aiohttp_cors
from aiohttp import web

class routes:
    def __init__(self, app):
        self.app = app

    def setup_routes(self):
        self.app.router.add_routes([
            web.get('/', self.home),
            web.get('/index', self.home),
            # web.get('/mashtun', self.getMashTunTemperature),
            # web.get('/mashtun/get/temperature', self.getMashTunTemperature),

            web.get('/mashtun/set/temperature/{degrees}', self.setMashTunTemperature),
            web.get('/mashtun/set/water/{liters}', self.setMashTunWaterLevel),
            web.get('/mashtun/set/time/{minutes}', self.setMashTunTime),

            web.get('/boilkettle/set/temperature/{degrees}', self.setBoilKettleTemperature),
            web.get('/boilkettle/set/water/{liters}', self.setBoilKettleWaterLevel),
            web.get('/boilkettle/set/time/{minutes}', self.setBoilKettleTime),
        ])

        # Configure default CORS settings.
        cors = aiohttp_cors.setup(self.app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers="*",
                )
        })
        # Configure CORS on all routes.
        for route in list(self.app.router.routes()):
            cors.add(route)


    def home(self, request):
        return web.json_response({'response': 'The Ragnarök is coming ...'})


    def setMashTunTemperature(self, request):
        degrees = request.match_info.get('degrees', 0)
        return web.json_response({'response': str(degrees)})
    

    def setMashTunWaterLevel(self, request):
        liters = request.match_info.get('liters', 0)
        return web.json_response({'response': str(liters)})
    
    
    def setMashTunTime(self, request):
        minutes = request.match_info.get('minutes', 0)
        return web.json_response({'response': str(minutes)})
    
    
    def setBoilKettleTemperature(self, request):
        degrees = request.match_info.get('degrees', 0)
        return web.json_response({'response': str(degrees)})
    
    
    def setBoilKettleWaterLevel(self, request):
        liters = request.match_info.get('liters', 0)
        return web.json_response({'response': str(liters)})
    
    
    def setBoilKettleTime(self, request):
        minutes = request.match_info.get('minutes', 0)
        return web.json_response({'response': str(minutes)})
    