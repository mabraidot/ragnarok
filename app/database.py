import sqlite3
from sqlite3 import Error
import json

class Database:
    def __init__(self, app, config):
        self.app = app
        self.config = config
        self.conn = None

        try:
            self.conn = sqlite3.connect('app/database/ragnarok.db')

            ## Create table Recipes if not exists
            cursor = self.conn.cursor()
            query = """
                CREATE TABLE IF NOT EXISTS recipes(
                    id INTEGER PRIMARY KEY NOT NULL,
                    name TEXT NOT NULL,
                    type_name TEXT NOT NULL,
                    style_name TEXT NULL,
                    style_category TEXT NULL,
                    original_gravity TEXT NULL,
                    final_gravity TEXT NULL,
                    ibu TEXT NULL,
                    abv TEXT NULL,
                    color TEXT NULL,
                    beer_json JSON NOT NULL,
                    cooked TEXT NULL,
                    created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """
            cursor.execute(query)
            self.conn.commit()

            query = """
                CREATE TABLE IF NOT EXISTS unfinished(
                    id INTEGER PRIMARY KEY NOT NULL,
                    recipe_id INTEGER NOT NULL,
                    process_name TEXT NOT NULL,
                    process_number INTEGER NOT NULL,
                    mash_total_time REAL NOT NULL,
                    mashtun_water_level REAL NOT NULL,
                    mashtun_time_probe REAL NOT NULL,
                    boilkettle_water_level REAL NOT NULL,
                    boilkettle_time_probe REAL NOT NULL
                )
            """
            cursor.execute(query)
            self.conn.commit()

        except Error:
            self.app.ws.setLog({self.config['LOG_ERROR_PERSISTENT_LABEL']: '[DB]: ' + Error})


    def insertRecipe(self, name, type_name, style_name, style_category, original_gravity, 
                    final_gravity, ibu, abv, color, beer_json):
        cursor = self.conn.cursor()
        query = """
            INSERT INTO recipes (
                name, type_name, style_name, style_category, original_gravity, 
                final_gravity, ibu, abv, color, beer_json
            ) 
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        entities = (name, type_name, style_name, style_category, original_gravity, 
                    final_gravity, ibu, abv, color, json.dumps(beer_json))
        cursor.execute(query, entities)
        self.conn.commit()


    def updateRecipe(self, id, name = None, type_name = None, style_name = None, style_category = None, 
                    original_gravity = None, final_gravity = None, ibu = None, abv = None, color = None, 
                    beer_json = None, cooked = None):
        params = locals()
        cursor = self.conn.cursor()

        columns = []
        entities = []
        for label, value in params.items():
            if label != 'id' and label != 'self' and value is not None:
                columns.append(label + ' = ?')
                entities.append(value)

        entities.append(id)
        query = "UPDATE recipes SET " + ", ".join(columns) + " WHERE id = ?"
        try:
            cursor.execute(query, entities)
            self.conn.commit()
        except Error:
            print(query, entities, Error)


    def listRecipes(self):
        cursor = self.conn.cursor()
        query = "SELECT *, DATETIME(cooked, 'localtime'), DATETIME(created, 'localtime') FROM recipes WHERE 1 ORDER BY created DESC"
        cursor.execute(query)
        rows = cursor.fetchall()

        recipes = {
            'unfinished': False,
            'totalRows': len(rows),
            'recipes': []
        }
        for row in rows:
            recipes['recipes'].append({
                'id':               row[0],
                'name':             row[1],
                'type_name':        row[2],
                'style_name':       row[3],
                'style_category':   row[4],
                'original_gravity': row[5],
                'final_gravity':    row[6],
                'ibu':              row[7],
                'abv':              row[8],
                'color':            row[9],
                'beer_json':        row[10],
                'cooked':           row[13],
                'created':          row[14],
            })

        recipes['unfinished'] = self.getUnfinishedRecipe()

        return json.dumps(recipes)

    def getRecipe(self, id):
        cursor = self.conn.cursor()
        query = "SELECT *, DATETIME(cooked, 'localtime'), DATETIME(created, 'localtime') FROM recipes WHERE id = ?"
        cursor.execute(query, id)
        row = cursor.fetchone()

        if row is not None:
            recipe = {
                    'id':               row[0],
                    'name':             row[1],
                    'type_name':        row[2],
                    'style_name':       row[3],
                    'style_category':   row[4],
                    'original_gravity': row[5],
                    'final_gravity':    row[6],
                    'ibu':              row[7],
                    'abv':              row[8],
                    'color':            row[9],
                    'beer_json':        json.loads(row[10]),
                    'cooked':           row[13],
                    'created':          row[14],
                }
        else:
            recipe = False

        return recipe


    def deleteRecipe(self, recipeId):
        cursor = self.conn.cursor()
        query = "DELETE FROM recipes WHERE id = ?"
        cursor.execute(query, recipeId)
        self.conn.commit()


    def getUnfinishedRecipe(self):
        cursor = self.conn.cursor()
        query = "SELECT * FROM unfinished WHERE 1 LIMIT 1"
        cursor.execute(query)
        row = cursor.fetchone()

        if row is not None:
            recipe = {
                    'id':                       row[0],
                    'recipe_id':                row[1],
                    'process_name':             row[2],
                    'process_number':           row[3],
                    'mash_total_time':          row[4],
                    'mashtun_water_level':      row[5],
                    'mashtun_time_probe':       row[6],
                    'boilkettle_water_level':   row[7],
                    'boilkettle_time_probe':    row[8],
                }
        else:
            recipe = False

        return recipe


    def insertUnfinishedRecipe(self, recipe_id, process_name, process_number, mash_total_time, 
                              mashtun_water_level, mashtun_time_probe, boilkettle_water_level, 
                              boilkettle_time_probe):
        cursor = self.conn.cursor()
        query = """
            INSERT OR REPLACE INTO unfinished (
                id, recipe_id, process_name, process_number, mash_total_time, 
                mashtun_water_level, mashtun_time_probe, boilkettle_water_level, boilkettle_time_probe
            ) 
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        entities = (1, recipe_id, process_name, process_number, mash_total_time, 
                    mashtun_water_level, mashtun_time_probe, boilkettle_water_level, 
                    boilkettle_time_probe)
        cursor.execute(query, entities)
        self.conn.commit()


    def deleteUnfinishedRecipe(self):
        cursor = self.conn.cursor()
        query = "DELETE FROM unfinished WHERE 1"
        cursor.execute(query)
        self.conn.commit()