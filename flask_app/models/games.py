from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Game:
    def __init__(self, data) :
        self.id = data["id"]
        self.name = data["name"]
        self.image = data["image"]
        self.genre = data["genre"]
        self.release_date = data["release_date"]
        self.pc = data["pc"]
        self.playstation_4 = data["playstation_4"]
        self.playstation_5 = data["playstation_5"]
        self.x_box = data["x_box"]
        self.switch = data["switch"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]



    # ****************  get all games    ***********
    @classmethod
    def get_all_games(cls, data):

        query = """
                    SELECT * FROM games
            """
        results = connectToMySQL(DATABASE).query_db(query, data)

        games_instances = []
        if results:
            for row in results:
                one_game = Game(row)
                games_instances.append(one_game)

            return games_instances        
        return []


















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