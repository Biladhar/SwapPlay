from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re

# regular expression for the email format
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.full_name = data["full_name"]
        self.username = data["username"]
        self.email = data["email"]
        self.password = data["password"]
        self.birthday= data["birthday"]
        self.phone_number= data["phone_number"]
        self.profile_image= data["profile_image"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    # save user into the DB
    @classmethod
    def create(cls, data):

        query = """
                INSERT INTO users (full_name, username, email, password,birthday,phone_number,profile_image)
                VALUES(%(full_name)s, %(username)s, %(email)s, %(password)s,%(birthday)s,%(phone_number)s,"user.jpg");
                """

        return connectToMySQL(DATABASE).query_db(query, data)

    # get a user by email
    @classmethod
    def get_by_email(cls, data):

        query = """
                    SELECT * FROM users
                    WHERE email = %(email)s;
            """
        result = connectToMySQL(DATABASE).query_db(query, data)

        if len(result) < 1:
            return False
        return User(result[0])

    # get a user by id
    @classmethod
    def get_by_id(cls, data):

        query = """
                    SELECT * FROM users
                    WHERE id = %(id)s;
            """
        result = connectToMySQL(DATABASE).query_db(query, data)

        if len(result) < 1:
            return False
        return User(result[0])
    
    # Add this method to your User class
    @classmethod
    def update(cls, data):
        query = """
                UPDATE users SET full_name = %(full_name)s, username = %(username)s, email = %(email)s, password = %(password)s,birthday= %(birthday)s,phone_number= %(phone_number)s, profile_image = %(profile_image)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_user(data):
        is_valid = True

        if len(data["full_name"]) < 2:
            is_valid = False
            flash("full name is required !", "register")

        if len(data["username"]) < 2:
            is_valid = False
            flash("username is required !", "register")

        if len(data["birthday"]) < 1:
            is_valid = False
            flash("birthday is required !", "register")

        if len(data["phone_number"]) < 8:
            is_valid = False
            flash("phone number is required !", "register")

        if len(data["email"]) < 1:
            is_valid = False
            flash("email is required !")
        # test whether a field matches the pattern
        elif not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email address!", "register")
            is_valid = False
        else:
            email_dict = {"email": data["email"]}
            potential_user = User.get_by_email(email_dict)
            if potential_user:
                is_valid = False
                flash("This email is already taken; Hopefully by you !", "register")

        if len(data["password"]) < 8:
            is_valid = False
            flash("password required", "register")

        elif not data["password"] == data["confirm_password"]:
            is_valid = False
            flash("passwords don't match !", "register")

        return is_valid

    @staticmethod
    def validate_login_user(data):
        is_valid = True

        if len(data["email"]) < 1:
            is_valid = False
            flash("email is required !", "login")
        # test whether a field matches the pattern
        elif not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email address!", "login")
            is_valid = False

        if len(data["password"]) < 8:
            is_valid = False
            flash("password is required !", "login")

        return is_valid