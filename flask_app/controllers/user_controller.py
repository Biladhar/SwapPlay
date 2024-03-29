from flask_app import app
from flask import redirect, render_template, request, flash, session
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os


from flask_app.models.games import Game
from flask_app.models.users import User

bcrypt = Bcrypt(app)


# ********* View Route ******************
# ********** LANDING PAGE ***************
@app.route("/")
def home():
    return render_template("landing_page.html")

# ************  REGISTRATION ******************
@app.route("/registration")
def reg():
    return render_template("registration_page.html")

# ************* LOGIN ****************************
@app.route("/login")
def log():
    return render_template("login.html")

# ? ************ ADMIN ***************
# **************  dashboard admin view route ***************
@app.route("/dashboard/admin")
def dash_admin():
    # verify if user is logged
    if "user_id" not in session:
        return redirect ("/")
    data ={
        "id" : session["user_id"]
    }
    user = User.get_by_id(data)
    if user.role != "admin":
        return redirect("/")
    nb_users=User.count_all_users()
    nb_games=Game.count_all_games()
    all_users=User.get_all_users()
    pending_swap = Swap.get_all_pending_swap()
    other_swaps = Swap.get_all_ar_swap()
    all_games=Game.get_all_games()
    return render_template("dashboard_admin.html",nb_users=nb_users,nb_games=nb_games,all_users=all_users,all_games=all_games,pending_swap=pending_swap,swaps = other_swaps)

# ?????????? search by name in user ?????????
@app.route("/search_name_users", methods = ["post"])
def search_users():
    # verify if user is logged
    if "user_id" not in session:
        return redirect ("/")
    # grab the user id from session and put in a dictionary
    data = {"full_name": request.form["full_name"]}
    # grab the user by id from DB
    
    by_name=User.search_by_name_of_users(data)
    by_name1=Game.search_by_name_of_games(data)
    nb_users=User.count_all_users()
    nb_games=Game.count_all_games()
    all_users=User.get_all_users()
    # grab the user id from session and put in a dictionary
    all_games=Game.get_all_games()
    return render_template("dashboard_admin.html",nb_users=nb_users,nb_games=nb_games,all_users=all_users,all_games=all_games,by_name=by_name,by_name1=by_name1)
    # return redirect("/dashboard/admin")
# ? *******************************************************

# ? ************   DASHBOARD ******************
# * dashboard view route
@app.route("/dashboard")
def dash():
    # verify if user is logged
    if "user_id" not in session:
        return redirect ("/")
    data ={
        'id':session['user_id']
    }
    user = User.get_by_id(data)
    if user.role == "admin":
        return redirect("/dashboard/admin")
    # grab the user id from session and put in a dictionary
    # grab the user id from session and put in a dictionary
    data2 = {"user_id": session["user_id"]}
    user_games = Game.get_one_user_games(data2)
<<<<<<< Updated upstream
    return render_template("dashboard.html", user = current_user, user_games = user_games  )
=======
    swaps = Swap.get_all_swaps_for_user(data)
    return render_template("dashboard.html", user = user, user_games = user_games ,swaps = swaps )










# ! action route : delete one user
@app.route("/delete/user/<int:id>",methods=['POST'])
def delete_by_id(id):
    if "user_id" not in session:
        return redirect("/")
    # fetch the user by id
    user_dict = {
        "id": id
    }
    User.delete_by_id(user_dict)
    return redirect("/dashboard/admin")



>>>>>>> Stashed changes



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

UPLOAD_FOLDER = 'C:/Users/kbeno/Desktop/py_project/SwapPlay/flask_app/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ************ EDIT USER ******************************
@app.route('/users/edit', methods=['GET', 'POST'])
def edit_user():
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
            pw_hash = bcrypt.generate_password_hash(request.form["password"])
            data = {
                "id": session['user_id'],
                "full_name": request.form['full_name'],
                "username": request.form['username'],
                "email": request.form['email'],
                # "password": request.form['password'],
                "birthday": request.form['birthday'],
                "phone_number": request.form['phone_number'],
                "password":pw_hash,
                "profile_image": filename
                
            }
            User.update(data)
            return redirect('/dashboard')
    return render_template('edit_user.html')


# *********** LOGOUT *************
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")



# @app.route("/users/edit/<int:id>")
# def edit_one(id):
#     if "user_id" not in session:
#         return redirect ("/")
#     data={
#         "id" : id
#     }
#     user=User.get_by_id(data)
#     return render_template("edit.html",user=user)

# @app.route("/edit/<int:id>", methods=["POST"])
# def edit_users(id):
#     pw_hash = bcrypt.generate_password_hash(request.form["password"])
#     print("**********************************",request.form)
#     data={
#         **request.form,
#         "password":pw_hash,
#         "id":id
#     }
#     User.edit(data)
#     return redirect("/dashboard")

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

