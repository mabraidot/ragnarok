import xmltodict
import datetime
from app.database import Database
import json as JSON

class Recipes:
    def __init__(self, app, config):
        self.app = app
        self.app.DB = Database(app, config)


    def importRecipe(self, xml):
        success = False
        try:
            json = xmltodict.parse(xml)
            if(json['RECIPES']['RECIPE']):
                name = json['RECIPES']['RECIPE']['NAME']
                type_name = json['RECIPES']['RECIPE']['STYLE']['TYPE']
                style_name = json['RECIPES']['RECIPE']['STYLE']['CATEGORY']
                style_category = json['RECIPES']['RECIPE']['STYLE']['CATEGORY_NUMBER']
                original_gravity = json['RECIPES']['RECIPE']['EST_OG']
                final_gravity = json['RECIPES']['RECIPE']['EST_FG']
                ibu = json['RECIPES']['RECIPE']['IBU']
                abv = json['RECIPES']['RECIPE']['ABV']
                color = json['RECIPES']['RECIPE']['EST_COLOR']
                beer_json = json

                self.app.DB.insertRecipe(name, type_name, style_name, style_category, original_gravity, 
                                            final_gravity, ibu, abv, color, beer_json)
                success = True
        except Exception as error:
            self.app.logger.info('[IMPORT RECIPE] %s', error)
            success = False

        return success


    def listRecipes(self):
        recipes = self.app.DB.listRecipes()
        return recipes


    def getRecipe(self, id):
        recipe = self.app.DB.getRecipe(id)

        return recipe


    def updateCookDate(self, recipeId):
        self.app.DB.updateRecipe(id=recipeId, cooked=datetime.datetime.now(datetime.timezone.utc))


    def deleteRecipe(self, recipeId):
        try:
            self.app.DB.deleteRecipe(recipeId)
            result = True
        except:
            result = False

        return result


    def getUnfinishedRecipe(self):
        recipe = self.app.DB.getUnfinishedRecipe()

        return recipe


    def updateUnfinishedRecipe(self, recipe_id, process_name, process_number, mash_total_time, 
        mashtun_water_level, mashtun_time_probe, boilkettle_water_level, boilkettle_time_probe):
        self.app.DB.insertUnfinishedRecipe(recipe_id, process_name, process_number, mash_total_time, 
                    mashtun_water_level, mashtun_time_probe, boilkettle_water_level, boilkettle_time_probe)


    def deleteUnfinishedRecipe(self):
        try:
            self.app.DB.deleteUnfinishedRecipe()
            result = True
        except:
            result = False

        return result