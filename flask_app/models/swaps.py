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
                VALUES(1, %(game_id)s, %(game1_id)s,%(game_user_id)s ,%(game1_user_id)s);
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
            game_offer=games.Game.get_one_game_with_id(data1)
            swap.game = game_offer

            game_selected=games.Game.get_one_game_with_id(data2)
            swap.game1 = game_selected

            user1=users.User.get_by_id(data3)
            swap.user1 = user1

            
            user=users.User.get_by_id(data4)
            swap.user = user

            all_swap.append(swap)
        return all_swap
    
<<<<<<< Updated upstream
=======
            # *get one swap by id
    @classmethod
    def get_one_swaps_by_id(cls, data):
        query = """
                SELECT *FROM swaps
                WHERE swaps.id = %(id)s ;
                """
        results = connectToMySQL(DATABASE).query_db(query, data)
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
            game_offer=games.Game.get_one_game_with_id(data1)
            swap.game = game_offer

            game_selected=games.Game.get_one_game_with_id(data2)
            swap.game1 = game_selected

            user1=users.User.get_by_id(data3)
            swap.user1 = user1

            
            user=users.User.get_by_id(data4)
            swap.user = user

        return swap



    @classmethod
    def accept_swap(cls, data):
        query = """
                UPDATE swaps SET status = 2 
                WHERE id = %(id)s ;
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def game_swap(cls, data):
        query = """
                UPDATE games SET user_id = (SELECT game1_user_id FROM swaps WHERE id = %(id)s) 
                WHERE id = (SELECT game_id FROM swaps WHERE id = %(id)s);
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def game1_swap(cls, data):
        query = """
                UPDATE games SET user_id = (SELECT game_user_id FROM swaps WHERE id = %(id)s)
                WHERE id = (SELECT game1_id FROM swaps WHERE id = %(id)s);
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def refuse_swap(cls, data):
        query = """
                UPDATE swaps SET status = 0 
                WHERE id = %(id)s ;
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    

    @classmethod
    def delete_game_with_swap(cls,data):
        query = """
            DELETE FROM swaps
            WHERE game_id=%(id)s OR game1_id=%(id)s
                """
        return connectToMySQL(DATABASE).query_db(query,data)
>>>>>>> Stashed changes
    
    @classmethod
    def delete_swap(cls,data):
        query = """
            DELETE FROM swaps
            WHERE id=%(id)s 
                """
        return connectToMySQL(DATABASE).query_db(query,data)


    @classmethod
    def get_all_pending_swap(cls):
        query = """
                SELECT * FROM swaps
                WHERE status = 1;
                """
        results = connectToMySQL(DATABASE).query_db(query)
        all_swap = []
        if results :
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
                game_offer=games.Game.get_one_game_with_id(data1)
                swap.game = game_offer

                game_selected=games.Game.get_one_game_with_id(data2)
                swap.game1 = game_selected

                user1=users.User.get_by_id(data3)
                swap.user1 = user1


                user=users.User.get_by_id(data4)
                swap.user = user

                all_swap.append(swap)
        return all_swap


    @classmethod
    def get_all_ar_swap(cls):
        query = """
                SELECT * FROM swaps
                WHERE status = 0 OR status = 2;
                """
        results = connectToMySQL(DATABASE).query_db(query)
        all_swap = []
        if results :
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
                game_offer=games.Game.get_one_game_with_id(data1)
                swap.game = game_offer
    
                game_selected=games.Game.get_one_game_with_id(data2)
                swap.game1 = game_selected
    
                user1=users.User.get_by_id(data3)
                swap.user1 = user1
    
                
                user=users.User.get_by_id(data4)
                swap.user = user
    
                all_swap.append(swap)
        return all_swap
