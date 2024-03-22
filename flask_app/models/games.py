<<<<<<< HEAD
=======
<<<<<<< Updated upstream
=======
>>>>>>> market_place
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
    
# * get all the game of one user
    @classmethod
    def get_one_user_games(cls, data2):

        query = """
                    SELECT * FROM games
                    WHERE games.user_id = %(user_id)s;
                """
        
        result = connectToMySQL(DATABASE).query_db(query, data2)
        no_game = []
        if len(result) < 1:
            return no_game
        return result
<<<<<<< HEAD
=======
    
    
    @classmethod
    def get_all_games(cls):
        query = """
                SELECT * FROM games;
                """
        results = connectToMySQL(DATABASE).query_db(query)
        all_games =[]
        for games in results :
            all_games.append(cls(games))
        return all_games
    
    @classmethod
    def get_all_state(cls, state):
        query = """
                SELECT * FROM SwapPlay.games WHERE state LIKE %(state)s;
                """

        results = connectToMySQL(DATABASE).query_db(query, state)
        print("*****************************",state)
        state_games =[]
        for state in results :
            state_games.append(cls(state))
        
        return state_games
>>>>>>> market_place

        
















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

<<<<<<< HEAD
        return is_valid
=======
        return is_valid
>>>>>>> Stashed changes
>>>>>>> market_place
