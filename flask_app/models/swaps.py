from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE


class Swap:
    def __init__(self, data) :
        self.id = data["id"]
        self.status = data["status"]
        self.game_id = data["game_id"]
        self.game1_id = data["game1_id"]
        self.game_user_id = data["game_user_id"]
        self.game1_user_id = data["game1_user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    # * create one swap
    @classmethod
    def create_swap(cls, data):
        query = """
                INSERT INTO swaps (status, game_id , game1_id ,game_user_id ,game1_user_id)
                VALUES(%(status)s, %(game_id)s, %(game1_id)s,%(game_user_id)s ,%(game1_user_id)s);
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    

        # *get all swap by user
    @classmethod
    def get_all_swaps_for_user(cls, data):
        query = """
                SELECT DISTINCT games.*, users.*
                FROM games
                JOIN swaps AS s1 ON games.id = s1.game_id OR games.id = s1.game1_id
                JOIN swaps AS s2 ON s1.id = s2.id
                JOIN users ON users.id = s2.game_user_id OR users.id = s2.game1_user_id
                WHERE (s1.game_user_id = %(id)s OR s1.game1_user_id = %(id)s)
                AND (users.id != %(id)s);
                """
        # OR 
        # query = """
        #         SELECT *FROM swaps
        #         WHERE game_user_id = %(id)s
        #         OR game1_user_id = %(id)s;
        #         """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    
    
    