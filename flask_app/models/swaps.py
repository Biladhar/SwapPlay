from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import users
from flask_app.models import games
from pprint import pprint


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
                SELECT *FROM swaps
                WHERE game_user_id = %(id)s
                OR game1_user_id = %(id)s;
                """
        results = connectToMySQL(DATABASE).query_db(query, data)
        all_swap = []
        for x in results:
            swap = Swap(x)
            data1 = {
                **x,
                "id":x['game_id']
            }
            data2 = {
                **x,
                "id":x['game1_id']
            }
            data3 = {
                **x,
                "id":x['game1_user_id']
            }
            data4 = {
                **x,
                "id":x['game_user_id']
            }
            game_offer=games.Game.get_game_id(data1)
            game = games.Game(game_offer[0])
            swap.game = game

            game_selected=games.Game.get_game_id(data2)
            game1 = games.Game(game_selected[0])
            swap.game1 = game1

            user1=users.User.get_by_id(data3)
            swap.user1 = user1

            
            user=users.User.get_by_id(data4)
            swap.user = user

            all_swap.append(swap)
        return all_swap
    
            # *get one swap by id
    @classmethod
    def get_one_swaps_by_id(cls, data):
        query = """
                SELECT *FROM swaps
                WHERE swaps.id = %(id)s ;
                """
        results = connectToMySQL(DATABASE).query_db(query, data)
        swap = Swap(results)
        
        data1 = {
                **results,
                "id":results['game_id']
            }
        data2 = {
                **results,
                "id":results['game1_id']
            }
        data3 = {
                **results,
                "id":results['game1_user_id']
            }
        data4 = {
                **results,
                "id":results['game_user_id']
            }
        game_offer=games.Game.get_game_id(data1)
        game = games.Game(game_offer[0])
        swap.game = game

        game_selected=games.Game.get_game_id(data2)
        game1 = games.Game(game_selected[0])
        swap.game1 = game1

        user1=users.User.get_by_id(data3)
        swap.user1 = user1

            
        user=users.User.get_by_id(data4)
        swap.user = user

        return swap

    @classmethod
    def accept_swap(cls, data):
        pass
    
    
    
    