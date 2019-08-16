from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.child.models import Child
from application.auth.forms import LoginForm, NewuserForm

@app.route("/auth", methods=["GET"])
def user_index():
    childrencount = User.how_many_children()
    child_in_all = Child.childrencount()
    user_in_all = User.usercount()
    
    return render_template("auth/userlist.html", childrencount = childrencount, child_in_all=child_in_all,user_in_all=user_in_all)

@app.route("/auth/newuser/")
def user_form():
    return render_template("auth/newuser.html", form = NewuserForm())

@app.route("/auth/", methods=["GET", "POST"])
def user_create():
    form = NewuserForm(request.form)
    
    if not form.validate():
        return render_template("auth/newuser.html", form = form)

    u = User(name = form.name.data, username = form.username.data, password = form.password.data)

    db.session().add(u)
    db.session().commit()  

    return  redirect(url_for("quotes_index"))

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    # validoinnit

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form,
                               error = "Käyttäjänimi tai salasana virheellinen")


    login_user(user)
    return redirect(url_for("index")) 

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index")) 