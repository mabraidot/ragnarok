import threading
import aiohttp_cors
from aiohttp import web

class routes:
    def __init__(self, app, config):
        self.app = app
        self.config = config

    def setup_routes(self):
        self.app.router.add_routes([
            web.get('/', self.home),
            web.get('/index', self.home),

            web.get('/cook/{recipe}', self.cook),

            web.post('/recipes/import', self.importRecipe),
            web.post('/recipes/list', self.listRecipes),
            web.get('/recipes/{recipe}/delete', self.deleteRecipe),
            
            web.get('/mashtun/set/temperature/{degrees}', self.setMashTunTemperature),
            web.get('/mashtun/set/water/{liters}', self.setMashTunWaterLevel),
            web.get('/mashtun/set/time/{minutes}', self.setMashTunTime),

            web.get('/mashtun/set/heater/{on}', self.setMashTunHeater),
            web.get('/mashtun/valve/set/inlet/{on}', self.setMashTunValveInlet),
            web.get('/mashtun/valve/set/outlet/{on}', self.setMashTunValveOutlet),

            web.get('/mashtun/PIDAutoTune', self.sartMashTunPIDAutoTune),

            web.get('/boilkettle/set/temperature/{degrees}', self.setBoilKettleTemperature),
            web.get('/boilkettle/set/water/{liters}', self.setBoilKettleWaterLevel),
            web.get('/boilkettle/set/time/{minutes}', self.setBoilKettleTime),

            web.get('/boilkettle/set/heater/{on}', self.setBoilKettleHeater),
            web.get('/boilkettle/valve/set/water/{on}', self.setBoilKettleValveWater),
            web.get('/boilkettle/valve/set/inlet/{on}', self.setBoilKettleValveInlet),
            web.get('/boilkettle/valve/set/outlet/{on}', self.setBoilKettleValveOutlet),

            web.get('/boilkettle/PIDAutoTune', self.sartBoilKettlePIDAutoTune),

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


    ## COOKING ############################

    async def cook(self, request):
        recipe = request.match_info.get('recipe', 0)
        self.app.cooking.start(recipe)

        return web.json_response({'notice': 'The cooking process started'})


    ## RECIPES ############################
    async def importRecipe(self, request):
        data = await request.post()
        response = {'error': 'XML data was empty'}
        if (data['file']):
            if self.app.recipes.importRecipe(data['file'].file):
                response = {'notice': 'XML received successfully'}

        return web.json_response(response)


    async def listRecipes(self, request):
        data = self.app.recipes.listRecipes()
        return web.json_response(data)
    

    async def deleteRecipe(self, request):
        recipe = request.match_info.get('recipe', 0)
        response = {'notice': 'Recipe was successfully deleted'}
        result = self.app.recipes.deleteRecipe(recipe)
        if not result:
            response = {'error': 'There was an error deleting the recipe'}
        return web.json_response(response)


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
        on = request.match_info.get('on', 'false')
        self.app.mashTun.setHeater(on)
        return web.json_response({'response': str(on)})
    
    def sartMashTunPIDAutoTune(self, request):
        message = {self.config['DEFAULT']['LOG_ERROR_LABEL']: 'A PID auto tunning process is already running'}
        if not self.app.mashTun.PIDAutoTune.running and not self.app.boilKettle.PIDAutoTune.running:
            message = {self.config['DEFAULT']['LOG_NOTICE_LABEL']: 'Starting a PID auto tunning process'}
            task = threading.Thread(target=self.app.mashTun.PIDAutoTune.run)
            task.start()
        return web.json_response(message)

    def setBoilKettleHeater(self, request):
        on = request.match_info.get('on', 'false')
        self.app.boilKettle.setHeater(on)
        return web.json_response({'response': str(on)})

    async def sartBoilKettlePIDAutoTune(self, request):
        message = {self.config['DEFAULT']['LOG_ERROR_LABEL']: 'A PID auto tunning process is already running'}
        if not self.app.mashTun.PIDAutoTune.running and not self.app.boilKettle.PIDAutoTune.running:
            message = {self.config['DEFAULT']['LOG_NOTICE_LABEL']: 'Starting a PID auto tunning process'}
            task = threading.Thread(target=self.app.boilKettle.PIDAutoTune.run)
            task.start()
        return web.json_response(message)


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
        on = request.match_info.get('on', 'false')
        self.app.pump.set(on)
        return web.json_response({'response': str(on)})