
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
        self.posted_by =users.User.get_by_id({"id":self.user_id})

    # ************** create one game ***********************
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
    
    # ******************* GET ALL STATE ********************
    @classmethod
    def get_all_state(cls, data):
        if data['state']=="any" and data['name']=='':
            query = """
                    SELECT * FROM games WHERE platform LIKE %(platform)s;
                    """
        elif data['platform']=="any" and data['name']=='':
            query = """
                    SELECT * FROM games WHERE state LIKE %(state)s;
                    """
        elif data['platform']=="any" and data['state']=="any":
            query = """
                    SELECT * FROM games WHERE name LIKE %(name)s;
                    """
        else:
            query = """
                    SELECT * FROM games WHERE platform LIKE %(platform)s
                    AND state LIKE %(state)s AND name LIKE %(name)s;
                    """




        results = connectToMySQL(DATABASE).query_db(query, data)

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
        user = User(results[0])
        game_dict={
            **results[0],
            "id":results[0]['games.id'],
            "created_at":results[0]['games.created_at'],
            "updated_at":results[0]['games.updated_at']
        }
        this_game = Game(game_dict)
        this_game.user =user       
        return this_game

    # ****************  GET ALL GAME with users ********************************
    @classmethod
    def get_all_games(cls):
        query = """
                SELECT * FROM users
                JOIN games ON users.id = games.user_id
                    
                """
        results = connectToMySQL(DATABASE).query_db(query)
        all_games =[]
        for x in results:
            user = users.User(x)
            data = {
                **x,
                "id":x['games.id'],
                "created_at":x['games.created_at'],
                "updated_at":x['games.updated_at']
            }
            game=cls(data)
            game.posted_by =user
            
            all_games.append(game)
        return all_games
    

       # ******** count all games ********************** 

    @classmethod
    def count_all_games(cls):
        query = "SELECT COUNT(*) as num FROM games;"
        results = connectToMySQL(DATABASE).query_db(query)
        return results[0]


    # ****************  DELETE GAME *****************************
    @classmethod
    def delete_game(cls,data):
        query="""
            DELETE FROM games 
            WHERE id=%(id)s
                """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    # **********  GET GAME BY NAME *******************

    @classmethod
    def search_by_name_of_games(cls,data):
        query = "SELECT * FROM games where name Like %(name)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        games_instances = []
        if results:
            for row in results:
                one_game = Game(row)
                games_instances.append(one_game)
        return games_instances


    # *****************  Game validation *************************

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

