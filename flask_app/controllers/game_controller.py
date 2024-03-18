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