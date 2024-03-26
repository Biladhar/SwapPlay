from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE


class Swap:
    def __init__(self, data) :
        self.id = data["id"]
        self.status = data["status"]
        self.game_id = data["game_id"]
        self.game1_id = data["game1_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    # * create one swap
    @classmethod
    def create_swap(cls, data):
        query = """
                INSERT INTO swaps (status, game_id,game1_id)
                VALUES(%(status)s, %(game_id)s, %(game1_id)s);
                """
        return connectToMySQL(DATABASE).query_db(query, data)