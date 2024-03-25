from flask_app import app
from flask import redirect, render_template, request, flash, session
from flask_app.models.games import Game
from flask_app.models.users import User
from werkzeug.utils import secure_filename
import os




# * View Route
@app.route("/marketplace")
def marketplace():
    games = Game.get_all_games()
    return render_template("marketplace.html" ,games = games)

UPLOAD_FOLDER = 'C:/Users/kbeno/Desktop/py_project/SwapPlay/flask_app/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/game/add", methods=["GET","POST"])
def new_game():

        if request.method == 'POST':
        # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # update user data in the database
                data = { 
                    **request.form,
                    "user_id":session["user_id"],
                    "image": filename
                    
                }
                Game.add(data)
                return redirect('/dashboard')
        return render_template('new_game.html')

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

# # * view route for the add new game form
# @app.route("/game/new")
# def add_game():
#     if "user_id" not in session:
#         return redirect ("/")
#     return render_template("new_game.html")


# # ! action route to create a new game
# @app.route("/game/add", methods=["GET","POST"])
# def new_game():
#         if not Game.validate_game(request.form):
#             return redirect("/game/new")
        
#         data = {    
#         **request.form,
#         "user_id":session["user_id"]
#         }
#         Game.add(data)
#         return redirect("/dashboard")

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

# * make offer
@app.route("/game/offer/<int:id>")
def offer(id):
    if "user_id" not in session:
        return redirect ("/")
    data={
        "id" : id
    }
    game1 = Game.get_one_game_with_user(data)
    data = {
        **request.form,
        "user_id": session["user_id"]
        }
    offers = Game.get_one_user_games(data)
    return render_template("offer.html",game1 =game1, offers=offers)

@app.route("/delete/<int:id>")
def delete_game_(id):
    data={
        "id" : id
    }
    Game.delete_game_user(data)
    return redirect("/dashboard")