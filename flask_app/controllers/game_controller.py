from flask_app import app
from flask import redirect, render_template, request, flash, session
from flask_app.models.games import Game
from flask_app.models.users import User



# * **************** VIEW ROUTE MARKET PLACE *********************
@app.route("/marketplace")
def marketplace():
    games = Game.get_all_games()
    return render_template("marketplace.html", games = games)


# ? =========  ADD GAME    ========================================
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
# ? ==================================================================


# ? =============   EDIT GAME   ==========================
# * view route edit game
@app.route("/game/edit/<int:id>")
def edit_game(id):
    if "user_id" not in session:
        return redirect ("/")
    data={
        "id" : id
    }
    game = Game.get_one_game_with_id(data)
    return render_template("edit_game.html",game=game)

# ! action route edit game
@app.route('/game/process/<int:id>', methods = ['POST'])
def edit_one_game(id):
    if not Game.validate_game(request.form):
        return redirect(f"/game/edit/{id}")
    data = {
        **request.form,
        "id" : id
    }

    Game.edit_game(data)
    return redirect("/dashboard")
# ? ======================================================

# ? =============    MAKE OFFER   ==========================
# * view route make offer
@app.route("/game/offer/<int:id>")
def offer(id):
    if "user_id" not in session:
        return redirect ("/")
    data={
        "id" : id
    }
    game1 = Game.get_one_game_with_user(data)
    data2 = {"user_id": session["user_id"]}
    offers = Game.get_one_user_games(data2)
    return render_template("offer.html",game1 =game1, offers=offers)