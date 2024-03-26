from flask_app import app
from flask import redirect, render_template, request, flash, session
from flask_app.models.games import Game
from flask_app.models.users import User


# * View Route
@app.route("/swap")
def pending_swap():
    
    return render_template("swap.html")