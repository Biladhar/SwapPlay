<<<<<<< Updated upstream
=======
from flask_app import app
from flask import redirect, render_template, request, flash, session
from flask_app.models.games import Game
from flask_app.models.users import User



# * view route for the add new game form
@app.route("/game/new")
def add_game():
    if "user_id" not in session:
        return redirect ("/")
    return render_template("new_game.html")

# ! action route to create a new game
@app.route("/game/add", methods=["POST"])
def new_game():
        if not Game.validate_game(request.form):
            return redirect("/game/new")
        data = {    
        **request.form,
        "user_id":session["user_id"]
        }
        Game.add(data)
        return redirect("/dashboard")

@app.route("/marketplace/show_games")
def show_all():
    if "user_id" not in session:
        return redirect ("/")
    data = {
        "id" : session["user_id"]
    }
    user = User.get_by_id(data)
    all_games = Game.get_all_games()
    return render_template("marketplace.html",all_games=all_games,user=user)

@app.route("/marketplace/show_by_state", methods=["POST"])
def show_state():
    if "user_id" not in session:
        return redirect ("/")
    data = {
        "id" : session["user_id"]
    }
    
    user = User.get_by_id(data)
    state_games = Game.get_all_state({"state" : request.form["state"]})
    return render_template("marketplace_state.html", state_games=state_games,user=user)
>>>>>>> Stashed changes
