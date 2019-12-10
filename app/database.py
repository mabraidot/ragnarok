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

        except Error:
            self.app.ws.setLog({self.config['LOG_ERROR_LABEL']: '[DB]: ' + Error})


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

# Retrieve json object: select json_extract(beer_json) from recipes;