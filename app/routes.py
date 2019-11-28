import aiohttp_cors
from aiohttp import web

class routes:
    def __init__(self, app):
        self.app = app

    def setup_routes(self):
        self.app.router.add_routes([
            web.get('/', self.home),
            web.get('/index', self.home),

            web.get('/mashtun/set/temperature/{degrees}', self.setMashTunTemperature),
            web.get('/mashtun/set/water/{liters}', self.setMashTunWaterLevel),
            web.get('/mashtun/set/time/{minutes}', self.setMashTunTime),

            web.get('/mashtun/set/heater/{on}', self.setMashTunHeater),
            web.get('/mashtun/valve/set/inlet/{on}', self.setMashTunValveInlet),
            web.get('/mashtun/valve/set/outlet/{on}', self.setMashTunValveOutlet),

            web.get('/boilkettle/set/temperature/{degrees}', self.setBoilKettleTemperature),
            web.get('/boilkettle/set/water/{liters}', self.setBoilKettleWaterLevel),
            web.get('/boilkettle/set/time/{minutes}', self.setBoilKettleTime),

            web.get('/boilkettle/set/heater/{on}', self.setBoilKettleHeater),
            web.get('/boilkettle/valve/set/water/{on}', self.setBoilKettleValveWater),
            web.get('/boilkettle/valve/set/inlet/{on}', self.setBoilKettleValveInlet),
            web.get('/boilkettle/valve/set/outlet/{on}', self.setBoilKettleValveOutlet),

            web.get('/chiller/set/water/{on}', self.setChillerValveWater),
            web.get('/chiller/set/wort/{on}', self.setChillerValveWort),

            web.get('/outlet/set/{on}', self.setOutletValve),
            web.get('/pump/set/{on}', self.setPump),

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

    ## MASH TUN ###########################
    def setMashTunTemperature(self, request):
        degrees = request.match_info.get('degrees', 0)
        self.app.mashTun.setTemperature(degrees)
        return web.json_response({'response': str(degrees)})
    

    def setMashTunWaterLevel(self, request):
        liters = request.match_info.get('liters', 0)
        self.app.mashTun.setWaterLevel(liters)
        return web.json_response({'response': str(liters)})
    
    
    def setMashTunTime(self, request):
        minutes = request.match_info.get('minutes', 0)
        return web.json_response({'response': str(minutes)})
    
    
    ## BOILER KETTLE #########################
    def setBoilKettleTemperature(self, request):
        degrees = request.match_info.get('degrees', 0)
        self.app.boilKettle.setTemperature(degrees)
        return web.json_response({'response': str(degrees)})
    
    
    def setBoilKettleWaterLevel(self, request):
        liters = request.match_info.get('liters', 0)
        self.app.boilKettle.setWaterLevel(liters)
        return web.json_response({'response': str(liters)})
    
    
    def setBoilKettleTime(self, request):
        minutes = request.match_info.get('minutes', 0)
        return web.json_response({'response': str(minutes)})


    ## HEATERS ###########################
    def setMashTunHeater(self, request):
        on = request.match_info.get('on', False)
        self.app.mashTun.setHeater(on)
        return web.json_response({'response': str(on)})


    def setBoilKettleHeater(self, request):
        on = request.match_info.get('on', False)
        self.app.boilKettle.setHeater(on)
        return web.json_response({'response': str(on)})


    ## VALVES ###########################
    def setMashTunValveInlet(self, request):
        on = request.match_info.get('on', 0)
        self.app.mashTunValveInlet.set(on)
        return web.json_response({'response': str(on)})


    def setMashTunValveOutlet(self, request):
        on = request.match_info.get('on', 0)
        self.app.mashTunValveOutlet.set(on)
        return web.json_response({'response': str(on)})


    def setBoilKettleValveWater(self, request):
        on = request.match_info.get('on', 0)
        self.app.boilKettleValveWater.set(on)
        return web.json_response({'response': str(on)})


    def setBoilKettleValveInlet(self, request):
        on = request.match_info.get('on', 0)
        self.app.boilKettleValveInlet.set(on)
        return web.json_response({'response': str(on)})


    def setBoilKettleValveOutlet(self, request):
        on = request.match_info.get('on', 0)
        self.app.boilKettleValveOutlet.set(on)
        return web.json_response({'response': str(on)})


    def setChillerValveWater(self, request):
        on = request.match_info.get('on', 0)
        self.app.chillerValveWater.set(on)
        return web.json_response({'response': str(on)})


    def setChillerValveWort(self, request):
        on = request.match_info.get('on', 0)
        self.app.chillerValveWort.set(on)
        return web.json_response({'response': str(on)})


    def setOutletValve(self, request):
        on = request.match_info.get('on', 0)
        self.app.outletValveDump.set(on)
        return web.json_response({'response': str(on)})


    ## PUMP #########################
    def setPump(self, request):
        on = request.match_info.get('on', False)
        self.app.pump.set(on)
        return web.json_response({'response': str(on)})