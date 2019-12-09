import xmltodict

class Recipes:
    def __init__(self, app):
        self.app = app

    def importRecipe(self, xml):
        success = False
        try:
            json = xmltodict.parse(xml)
            if(json['RECIPES']['RECIPE']):
                # @TODO: Save recipe JSON to Database
                print(json['RECIPES']['RECIPE']['NAME'])
                success = True
        except:
            success = False

        return success