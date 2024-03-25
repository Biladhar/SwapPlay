
from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from pprint import pprint
from flask_app.models import users
from flask_app.models.users import User

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
    
    # ******************   READ ALL GAMES **************************************

    @classmethod
    def get_all_games(cls):

        query = "SELECT * FROM games;"

        results = connectToMySQL(DATABASE).query_db(query)

        # print(results)

        games_instances = []
        if results:
            for row in results:
                one_game = Game(row)
                games_instances.append(one_game)

            return games_instances
        
        return []
    
    # ******************   EDIT GAME **************************************
    @classmethod
    def edit_game(cls,data):
        query="""
                UPDATE games
                SET name=%(name)s, state=%(state)s, image= %(image)s, platform=%(platform)s
                WHERE id= %(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    # ********************* GET ONE GAME WITH ID ***********************
    @classmethod
    def get_one_game_with_id(cls, data):

        query = """
                    SELECT * FROM games
                    WHERE games.id = %(id)s;
                """
        
        result = connectToMySQL(DATABASE).query_db(query, data)
        return Game(result[0])
    

# ********************** GET ALL GAMES OF 1 USER ***********************
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

    
# ******************   READ GAME WITH USER **************************************
    @classmethod
    def get_one_game_with_user(cls, data):

        query = """
                    SELECT * FROM users
                    JOIN games ON users.id = games.user_id
                    WHERE games.id = %(id)s;
                """
        
        results = connectToMySQL(DATABASE).query_db(query, data)
        pprint(results)
        this_game = Game(results[0])
        this_game.user = User(results[0])
        print(this_game)        
        return this_game

    @classmethod
    def get_all_games(cls):
        query = """
                SELECT * FROM users
                JOIN games ON users.id = games.user_id
                    
                """
        results = connectToMySQL(DATABASE).query_db(query)
        print(f"RECIPES_WITH_USERS: ----{results}")
        all_games =[]
        for x in results:
            game = cls(x)
            data = {
                **x,
                "id":x['games.id'],
                "created_at":x['games.created_at'],
                "updated_at":x['games.updated_at']
            }
            game.posted_by = users.User(data)
            game.gameid= users.User(data)
            all_games.append(game)
        return all_games

    @classmethod
    def delete_game_user(cls,data):
        query="""
                DELETE FROM games 
                WHERE id=%(id)s
                """
        return connectToMySQL(DATABASE).query_db(query,data)



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
        # if len(data["image"]) < 3:
        #     is_valid = False
        #     flash("image is required", "game")

        return is_valid

