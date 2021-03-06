import threading
import aiohttp_cors
from aiohttp import web

class routes:
    def __init__(self, app, config):
        self.app = app
        self.config = config

    def setup_routes(self):
        self.app.router.add_routes([
            web.get('/index', self.home),
            web.get('/', self.home),

            web.get('/cook/resume', self.cookResume),
            web.get('/cook/pause', self.cookPause),
            web.get('/cook/stop', self.cookStop),
            web.get('/cook/delete', self.cookUnfinishedDelete),
            web.get('/cook/{recipe}/resume', self.cookUnfinishedResume),
            web.get('/cook/{recipe}', self.cook),
            
            web.get('/clean/short', self.cleanShort),
            web.get('/clean/sanitization', self.cleanSanitization),
            web.get('/clean/full', self.cleanFull),
            web.get('/clean/stop', self.cleanStop),
            web.get('/clean/pause', self.cleanPause),

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
            web.get('/boilkettle/valve/set/return/{on}', self.setBoilKettleValveReturn),
            web.get('/boilkettle/valve/set/inlet/{on}', self.setBoilKettleValveInlet),
            web.get('/boilkettle/valve/set/outlet/{on}', self.setBoilKettleValveOutlet),

            web.get('/boilkettle/PIDAutoTune', self.sartBoilKettlePIDAutoTune),
            web.get('/valves/open', self.openAllValves),

            web.get('/chiller/set/water/{on}', self.setChillerValveWater),
            web.get('/chiller/set/wort/{on}', self.setChillerValveWort),

            web.get('/outlet/set/{on}', self.setOutletValve),
            web.get('/pump/set/{on}', self.setPump),

            web.get('/power/off', self.setPowerOff),
            web.get('/sounds/stop', self.stopSounds),

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




    ## MACHINE ############################

    async def setPowerOff(self, request):
        message = {self.config['DEFAULT']['LOG_NOTICE_LABEL']: 'The machine is turning off'}
        self.app.power.setOff()
        return web.json_response(message)

    async def stopSounds(self, request):
        message = {self.config['DEFAULT']['LOG_NOTICE_LABEL']: 'The sounds are shutted off'}
        self.app.sound.stop()
        return web.json_response(message)



    ## COOKING ############################

    async def cook(self, request):
        recipe = request.match_info.get('recipe', 0)
        message = {self.config['DEFAULT']['LOG_NOTICE_LABEL']: 'The cooking process started'}
        if self.app.cleaning.isRunning():
            message = {self.config['DEFAULT']['LOG_ERROR_LABEL']: 'A cleaning process is running'}
        else:
            self.app.cooking.start(int(recipe))

        return web.json_response(message)


    async def cookResume(self, request):
        message = {self.config['DEFAULT']['LOG_NOTICE_LABEL']: 'The cooking process was resumed'}
        if self.app.cleaning.isRunning():
            message = {self.config['DEFAULT']['LOG_ERROR_LABEL']: 'A cleaning process is running'}
        else:
            self.app.cooking.setNextStep()

        return web.json_response(message)


    async def cookPause(self, request):
        if not self.app.cooking.isRunning():
            message = {self.config['DEFAULT']['LOG_ERROR_LABEL']: 'Cooking process is not running'}
        else:
            if self.app.cooking.isPaused():
                message = {self.config['DEFAULT']['LOG_NOTICE_LABEL']: 'The cooking process was resumed'}
            else:
                message = {self.config['DEFAULT']['LOG_NOTICE_LABEL']: 'The cooking process was paused'}
            self.app.cooking.pause()

        return web.json_response(message)


    async def cookStop(self, request):
        self.app.cooking.stop()

        return web.json_response({self.config.get('DEFAULT', 'LOG_NOTICE_LABEL'): 'The cooking process was stopped'})


    async def cookUnfinishedDelete(self, request):
        response = {self.config.get('DEFAULT', 'LOG_NOTICE_LABEL'): 'Unfinished process was successfully deleted'}
        result = self.app.recipes.deleteUnfinishedRecipe()
        if not result:
            response = {self.config.get('DEFAULT', 'LOG_ERROR_LABEL'): 'There was an error deleting the process'}
        return web.json_response(response)


    async def cookUnfinishedResume(self, request):
        recipe = request.match_info.get('recipe', 0)
        self.app.cooking.resume(int(recipe))

        return web.json_response({self.config.get('DEFAULT', 'LOG_NOTICE_LABEL'): 'The unfinished cooking process was resumed'})


    ## RECIPES ############################
    async def importRecipe(self, request):
        data = await request.post()
        response = {self.config.get('DEFAULT', 'LOG_ERROR_LABEL'): 'XML data was empty'}
        if (data['file']):
            from app.recipes import Recipes
            self.app.recipes = Recipes(self.app, self.config)
            if self.app.recipes.importRecipe(data['file'].file):
                response = {self.config.get('DEFAULT', 'LOG_NOTICE_LABEL'): 'XML received successfully'}

        return web.json_response(response)


    async def listRecipes(self, request):
        from app.recipes import Recipes
        self.app.recipes = Recipes(self.app, self.config)
        data = self.app.recipes.listRecipes()
        return web.json_response(data)
    

    async def deleteRecipe(self, request):
        from app.recipes import Recipes
        self.app.recipes = Recipes(self.app, self.config)
        recipe = request.match_info.get('recipe', 0)
        response = {self.config.get('DEFAULT', 'LOG_NOTICE_LABEL'): 'Recipe '+str(recipe)+' was successfully deleted'}
        result = self.app.recipes.deleteRecipe(int(recipe))
        if not result:
            response = {self.config.get('DEFAULT', 'LOG_ERROR_LABEL'): 'There was an error deleting the recipe'}
        return web.json_response(response)


    ## MASH TUN ###########################
    def setMashTunTemperature(self, request):
        degrees = request.match_info.get('degrees', 0)
        self.app.mashTun.setTemperature(degrees)
        return web.json_response({'response': str(degrees)})
    

    def setMashTunWaterLevel(self, request):
        liters = request.match_info.get('liters', 0)
        # self.app.mashTun.setWaterLevel(liters)
        self.app.mashTun.setPriorWaterLevel(liters)
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
        # self.app.boilKettle.setWaterLevel(liters)
        self.app.boilKettle.setPriorWaterLevel(liters)
        return web.json_response({'response': str(liters)})
    
    
    def setBoilKettleTime(self, request):
        minutes = request.match_info.get('minutes', 0)
        return web.json_response({'response': str(minutes)})


    ## HEATERS ###########################
    def setMashTunHeater(self, request):
        on = request.match_info.get('on', 'false')
        if self.app.mashTun.getWaterLevel() > self.config.getfloat('DEFAULT', 'SAFE_WATER_LEVEL_FOR_HEATERS'):
            self.app.mashTun.setHeater(on)
        else:
            self.app.ws.setLog({
                self.config.get('DEFAULT', 'LOG_ERROR_LABEL'): 
                self.config.get('DEFAULT', 'SAFE_WATER_LEVEL_FOR_HEATERS') + ' liters of water are required to turn on heaters'
            })
        if on == 'false':
            self.app.mashTun.setTemperature(0)
        return web.json_response({'response': str(on)})
    
    def sartMashTunPIDAutoTune(self, request):
        message = {self.config['DEFAULT']['LOG_ERROR_LABEL']: 'A PID auto tunning process is already running'}
        if self.app.cooking.isRunning() or self.app.cleaning.isRunning():
            message = {self.config['DEFAULT']['LOG_ERROR_LABEL']: 'A cooking or cleaning process is running'}
        elif not self.app.mashTun.PIDAutoTune.running and not self.app.boilKettle.PIDAutoTune.running:
            message = {self.config['DEFAULT']['LOG_NOTICE_LABEL']: 'Starting a PID auto tunning process'}
            task = threading.Thread(target=self.app.mashTun.PIDAutoTune.run)
            task.start()
        return web.json_response(message)

    def setBoilKettleHeater(self, request):
        on = request.match_info.get('on', 'false')
        if self.app.boilKettle.getWaterLevel() > self.config.getfloat('DEFAULT', 'SAFE_WATER_LEVEL_FOR_HEATERS'):
            self.app.boilKettle.setHeater(on)
        else:
            self.app.ws.setLog({
                self.config.get('DEFAULT', 'LOG_ERROR_LABEL'): 
                self.config.get('DEFAULT', 'SAFE_WATER_LEVEL_FOR_HEATERS') + ' liters of water are required to turn on heaters'
            })
        if on == 'false':
            self.app.boilKettle.setTemperature(0)
        return web.json_response({'response': str(on)})

    async def sartBoilKettlePIDAutoTune(self, request):
        message = {self.config['DEFAULT']['LOG_ERROR_LABEL']: 'A PID auto tunning process is already running'}
        if self.app.cooking.isRunning() or self.app.cleaning.isRunning():
            message = {self.config['DEFAULT']['LOG_ERROR_LABEL']: 'A cooking or cleaning process is running'}
        elif not self.app.mashTun.PIDAutoTune.running and not self.app.boilKettle.PIDAutoTune.running:
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


    def setBoilKettleValveReturn(self, request):
        on = request.match_info.get('on', 0)
        self.app.boilKettleValveReturn.set(on)
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


    def openAllValves(self, request):
        message = {self.config['DEFAULT']['LOG_NOTICE_LABEL']: 'Open all valves'}
        if self.app.cooking.isRunning() or self.app.cleaning.isRunning():
            message = {self.config['DEFAULT']['LOG_ERROR_LABEL']: 'A cooking or cleaning process is running'}
        else:
            task = threading.Thread(target=self.app.pump.openAllVaves)
            task.start()
        return web.json_response(message)


    ## PUMP #########################
    def setPump(self, request):
        on = request.match_info.get('on', 'false')
        self.app.pump.set(on)
        return web.json_response({'response': str(on)})


    ## CLEANING ############################

    async def cleanShort(self, request):
        message = {self.config['DEFAULT']['LOG_NOTICE_LABEL']: 'The cleaning process started'}
        if self.app.cooking.isRunning() or self.app.cleaning.isRunning():
            message = {self.config['DEFAULT']['LOG_ERROR_LABEL']: 'A cooking or cleaning process is running'}
        else:
            self.app.cleaning.startShort()
        return web.json_response(message)

    async def cleanSanitization(self, request):
        message = {self.config['DEFAULT']['LOG_NOTICE_LABEL']: 'The cleaning process started'}
        if self.app.cooking.isRunning() or self.app.cleaning.isRunning():
            message = {self.config['DEFAULT']['LOG_ERROR_LABEL']: 'A cooking or cleaning process is running'}
        else:
            self.app.cleaning.startSanitization()
        return web.json_response(message)

    async def cleanFull(self, request):
        message = {self.config['DEFAULT']['LOG_NOTICE_LABEL']: 'The cleaning process started'}
        if self.app.cooking.isRunning() or self.app.cleaning.isRunning():
            message = {self.config['DEFAULT']['LOG_ERROR_LABEL']: 'A cooking or cleaning process is running'}
        else:
            self.app.cleaning.startFull()
        return web.json_response(message)


    async def cleanStop(self, request):
        self.app.cleaning.stop()

        return web.json_response({self.config.get('DEFAULT', 'LOG_NOTICE_LABEL'): 'The cleaning process was stopped'})

    async def cleanPause(self, request):
        if not self.app.cleaning.isRunning():
            message = {self.config['DEFAULT']['LOG_ERROR_LABEL']: 'Cleaning process is not running'}
        else:
            if self.app.cleaning.isPaused():
                message = {self.config['DEFAULT']['LOG_NOTICE_LABEL']: 'The cleaning process was resumed'}
            else:
                message = {self.config['DEFAULT']['LOG_NOTICE_LABEL']: 'The cleaning process was paused'}
            self.app.cleaning.pause()

        return web.json_response(message)