from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Game:
    def __init__(self, data) :
        self.id = data["id"]
        self.name = data["name"]
        self.state = data["state"]
        self.image = data["image"]
        self.platform = data["platform"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

# * create one game
    @classmethod
    def add(cls, data):
        query = """
                INSERT INTO games (name, state,image,platform,user_id)
                VALUES(%(name)s, %(state)s, %(image)s,%(platform)s,%(user_id)s);
                """
        return connectToMySQL(DATABASE).query_db(query, data)















    @staticmethod
    def validate_game(data):
        is_valid = True
        if len(data["name"]) < 3:
            is_valid = False
            flash("name is required !", "game")
        if len(data["platform"]) < 3:
            is_valid = False
            flash("platform is required", "game")
        if len(data["state"]) < 3 :
            is_valid = False
            flash("state is required", "game")
        if len(data["image"]) < 3:
            is_valid = False
            flash("image is required", "game")

        return is_valid