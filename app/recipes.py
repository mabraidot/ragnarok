import xmltodict

class Recipes:
    def __init__(self, app):
        self.app = app

    def importRecipe(self, xml):
        success = False
        # try:
        json = xmltodict.parse(xml)
        if(json['RECIPES']['RECIPE']):
            # @TODO: Save recipe JSON to Database
            # print(json['RECIPES']['RECIPE']['NAME'])
            name = json['RECIPES']['RECIPE']['NAME']
            type_name = json['RECIPES']['RECIPE']['STYLE']['TYPE']
            style_name = json['RECIPES']['RECIPE']['STYLE']['CATEGORY']
            style_category = json['RECIPES']['RECIPE']['STYLE']['CATEGORY_NUMBER'] + '.' + \
                             json['RECIPES']['RECIPE']['STYLE']['STYLE_LETTER']
            original_gravity = json['RECIPES']['RECIPE']['EST_OG']
            final_gravity = json['RECIPES']['RECIPE']['EST_FG']
            ibu = json['RECIPES']['RECIPE']['IBU']
            abv = json['RECIPES']['RECIPE']['ABV']
            color = json['RECIPES']['RECIPE']['EST_COLOR']
            beer_json = json

            self.app.DB.insertRecipe(name, type_name, style_name, style_category, original_gravity, 
                                          final_gravity, ibu, abv, color, beer_json)
            success = True
        # except:
        #     success = False

        return success