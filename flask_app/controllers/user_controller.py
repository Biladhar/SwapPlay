from flask_app import app
from flask import redirect, render_template, request, flash, session
from flask_bcrypt import Bcrypt


from flask_app.models.games import Game
from flask_app.models.users import User

bcrypt = Bcrypt(app)


# * View Route
@app.route("/")
def home():
    return render_template("landing_page.html")


@app.route("/login")
def log():
    return render_template("login.html")


# ? ==============  dashboard view route ====================

# * dashboard view route
@app.route("/dashboard")
def dash():
    # verify if user is logged
    if "user_id" not in session:
        return redirect ("/")
    # grab the user id from session and put in a dictionary
    data = {"id": session["user_id"]}
    # grab the user by id from DB
    current_user = User.get_by_id(data)
    # grab the user id from session and put in a dictionary
    data2 = {"user_id": session["user_id"]}
    user_games = Game.get_one_user_games(data2)
    return render_template("dashboard.html", user = current_user, user_games = user_games  )



@app.route("/registration")
def reg():
    return render_template("registration_page.html")

#! ACTION ROUTE
# === Register ===
@app.route("/register", methods=["POST"])
def process_register():

    # validate the form here ...
    if not User.validate_user(request.form):
        return redirect("/registration")
    # create the hash
    print("-------->", request.form["password"])
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    print("=======>", pw_hash)
    # User.create(request.form)
    data = {**request.form, "password": pw_hash}
    # store the user id inside the session
    user_id = User.create(data)
    session["user_id"] = user_id
    return redirect("/dashboard")




#! ACTION ROUTE
# === Login ===
@app.route("/login", methods=["POST"])
def process_login():

    if not User.validate_login_user(request.form):
        return redirect("/login")

    # see if the username provided exists in the database
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        # if we get False after checking the password
        flash("Invalid Email/Password", "login")
        return redirect("/")

    # get the user by his email
    session["user_id"] = user_in_db.id
    return redirect("/dashboard")

# ? ***************** EDIT PROFILE ***************
# * view route edit profile
@app.route("/users/edit/<int:id>")
def edit_one(id):
    if "user_id" not in session:
        return redirect ("/")
    data={
        "id" : id
    }
    user=User.get_by_id(data)
    return render_template("edit.html",user=user)


# ! action route edit profile
@app.route("/edit/<int:id>", methods=["POST"])
def edit_users(id):
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    print("**********************************",request.form)
    data={
        **request.form,
        "password":pw_hash,
        "id":id
    }
    User.edit(data)
    return redirect("/dashboard")
# ? ********************************************************************
# # * View Route
# @app.route("/dashboard")
# def dash():
#     #! ROUTE GUARD
#     if "user_id" not in session:
#         return redirect("/")
#     # grab the user id from session and put in a dictionary
#     data = {"id": session["user_id"]}
#     # grab the user by id from DB
#     current_user = User.get_by_id(data)
#     print("===> current_user:", current_user)
#     return render_template("dashboard.html", username=current_user.first_name)


# LOGOUT


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")