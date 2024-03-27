from flask_app import app
from flask import redirect, render_template, request, flash, session
from flask_app.models.games import Game
from flask_app.models.users import User
from flask_app.models.swaps import Swap


# * View Route
@app.route("/swap")
def pending_swap():
    data = {
        'id' : session["user_id"]
    }
    all_swaps = Swap.get_all_swaps_for_user(data)
    # print(all_swaps)
    user = User.get_by_id(data)
    
    return render_template("swap.html",swaps =all_swaps, user = user)



# # * view route
# @app.route("/swap/<int:id>")
# def swap_contact(id):
#     data = {
#         'id' : id
#     }
#     swap = Swap.get_one_swaps_by_id(data)
#     return render_template("end_swap.html",swap = swap )
# # ! action route Accept swap
# @app.route("/swap/process", methods = ['POST'])
# def swap_contact(id):
#     if "user_id" not in session:
#         return redirect ("/")
#     data={
#         "id" : id
#     }
#     Swap.get_one_swaps_by_id(data)

#     return redirect("/swap_contact")

