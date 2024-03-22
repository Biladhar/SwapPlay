from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Offer:
    def __init__(self, data) :
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.game_id = data["game_id"]
        self.platform = data["platform"]
        self.state = data["state"]
        self.offer_status = data["offer_status"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
