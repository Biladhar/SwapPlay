from flask_app import app
from flask import redirect, render_template, request, flash, session
from flask_app.models.games import Game
from flask_app.models.users import User


<<<<<<< Updated upstream
=======
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


# * view route
@app.route("/swap/<int:id>")
def swap_contact(id):
    data = {
        'id' : id
    }
    swap = Swap.get_one_swaps_by_id(data)
    return render_template("end_swap.html", swap = swap)


# ! action route Accept swap
@app.route("/swap/process", methods = ['POST'])
def swap_process():
    if "user_id" not in session:
        return redirect ("/")
    data={
        **request.form,
        'id' : request.form['swap_id']
    }
    Swap.accept_swap(data)
    Swap.game1_swap(data)
    Swap.game_swap(data)
    print("***********************",)
    return redirect(f"/swap/{request.form['swap_id']}")


# ! action route refuse swap
@app.route("/swap/refuse", methods = ['POST'])
def swap_refuse():
    if "user_id" not in session:
        return redirect ("/")
    print(request.form)
    data={
        **request.form,
        'id' : request.form['swap_id']
    }
    Swap.refuse_swap(data)
    print("***********************")
    return redirect("/swap")

# ! action delete swap
@app.route("/delete/swap/<int:id>")
def delete_a_swap(id):
    data={
        "id" : id
    }
    Swap.delete_swap(data)

    return redirect("/dashboard/admin")

# # * view route
# @app.route("/swap/<int:id>")
# def swap_contact(id):
#     data = {
#         'id' : id
#     }
#     swap = Swap.get_one_swaps_by_id(data)
#     return render_template("end_swap.html",swap = swap )

>>>>>>> Stashed changes
