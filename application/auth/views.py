from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

from application import app, db, login_required
from application.auth.models import User
from application.child.models import Child
from application.quotes.models import Quote
from application.likes.models import Likes
from application.auth.forms import LoginForm, NewuserForm, MakeSureFormUser

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

    alreadyExistsUser = User.query.filter_by(username=form.username.data).first()
    if alreadyExistsUser:
        form.username.errors.append("käyttäjätunnus on jo olemassa, valitse toinen käyttäjätunnus")
        return render_template("auth/newuser.html", form = form)

    u = User(name = form.name.data, username = form.username.data, password = form.password.data, role = "USER")

    username = form.username.data
    if username == "admin":
        u = User(name = form.name.data, username = form.username.data, password = form.password.data, role = "ADMIN")
    

    db.session().add(u)
    db.session().commit()  

    return  redirect(url_for("auth_login"))

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    

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

@app.route("/auth/<user_id>/delete", methods=["POST","GET"])
@login_required(role="ADMIN")
def user_delete(user_id):

   
    form = MakeSureFormUser()

    return render_template("auth/deleteuser.html", form = form, user_id=user_id)

@app.route("/auth/<user_id>/del", methods=["POST"])
@login_required(role="ADMIN")
def user_deleteConfirm(user_id):

    form = MakeSureFormUser(request.form)
    ok = form.name.data
    
    if ok == "x":

        user = User.query.filter(User.id == user_id).first()

        # Etsitään kaikki käyttäjän lapset
        children = Child.query.filter(Child.account_id == user_id)

        for c in children:
            # Etsitään kaikki lapsen sanonnat ja poistetaan ne, poistetaan lapsi tietokannasta
            c_id=c.id
            q = Quote.query.filter(Quote.child_id == c_id)
          
            for quote in q: 
            
                

                # Etsitään kaikki sanontoihin liittyvät tykkäykset ja poistetaan ne
                likes = Likes.query.filter(Likes.quote_id == quote.id)
                
                for like in likes:
                    db.session.delete(like)
                    
                db.session().delete(quote)
                db.session().commit()
                    
            db.session().delete(c)
            db.session().commit()
        
        # Poistetaan käyttäjän omat tykkäykset
        likesAccount = Likes.query.filter(Likes.account_id == user_id)
        for like in likesAccount:
                    db.session.delete(like)
                    db.session().commit()

        # Poistetaan lopuksi käyttäjä
        db.session().delete(user)
        db.session().commit()
        flash("Käyttäjä poistettu onnistuneesti", category="success")
        return redirect(url_for("user_index"))
    
    flash("Käyttäjää ei poistettu", category="warning")
    return redirect(url_for("user_index"))