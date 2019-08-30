from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

from application import app, db, login_required, bcrypt
from application.auth.models import User
from application.child.models import Child
from application.quotes.models import Quote
from application.likes.models import Likes
from application.auth.forms import LoginForm, UserForm, MakeSureFormUser

@app.route("/auth", methods=["GET"])
@login_required(role="ADMIN")
def user_index():
    # Lasketaan käyttäjälistaukseen käyttäjien omat lapsimäärät, kaikkien lasten määrä sekä  käyttäjien määrä
    childrencount = User.how_many_children()
    child_in_all = Child.childrencount()
    user_in_all = User.usercount()
    
    return render_template("auth/userlist.html", childrencount = childrencount, child_in_all=child_in_all,user_in_all=user_in_all)

@app.route("/auth/newuser/")
def user_form():
    return render_template("auth/newuser.html", form = UserForm())

@app.route("/auth/", methods=["GET", "POST"])
def user_create():
    form = UserForm(request.form)
    
    if not form.validate():
        return render_template("auth/newuser.html", form = form)

    # Tarkastetaan onko samanniminen käyttäjä jo olemassa
    alreadyExistsUser = User.query.filter_by(username=form.username.data).first()
    if alreadyExistsUser:
        form.username.errors.append("käyttäjätunnus on jo olemassa, valitse toinen käyttäjätunnus")
        return render_template("auth/newuser.html", form = form)

    # Salasanan salaus
    pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    u = User(name = form.name.data, username = form.username.data, password = pw_hash, role = "USER")

    username = form.username.data
    if username == "admin":
        u = User(name = form.name.data, username = form.username.data, password = pw_hash, role = "ADMIN")
    

    db.session().add(u)
    db.session().commit() 
    flash("Rekisteröinti onnistunut. Uusi käyttäjä käyttäjätunnuksella " +username+ " luotu.", category="success") 

    return  redirect(url_for("auth_login"))

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    
    user = User.query.filter_by(username=form.username.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form,
                               error = "Käyttäjänimi tai salasana virheellinen")

    password = form.password.data
    
    
    if not bcrypt.check_password_hash(user.password, password):
        return render_template("auth/loginform.html", form = form,
                               error = "käyttäjänimi tai salasana virheellinen")


    login_user(user)
    return redirect(url_for("index")) 

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index")) 

@app.route("/auth/<user_id>/delete", methods=["POST","GET"])
@login_required(role="ADMIN")
def user_delete(user_id):
   
    # Tarkistuslomake, jotta käyttäjää ei poisteta liian helpolla
    form = MakeSureFormUser()

    return render_template("auth/deleteuser.html", form = form, user_id=user_id)

@app.route("/auth/<user_id>/del", methods=["POST"])
@login_required(role="ADMIN")
def user_deleteConfirm(user_id):

    form = MakeSureFormUser(request.form)
    ok = form.name.data
    
    # Jos tarkistuslomakkeella on varmistettu käyttäjän poisto
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

@app.route("/auth/showuser/<user_id>", methods=["GET"])
@login_required(role="ANY")
def user_show(user_id):

    user = User.query.get(user_id)
    children = Child.query.filter(Child.account_id == user_id)
    
    return render_template("auth/showuser.html", children=children, user = user)

@app.route("/auth/updateuser/<user_id>", methods=["GET","POST"])
@login_required(role="ANY")
def user_update(user_id):
    #asetetaan lomakkeelle valmiiksi olevat tiedot paitsi salasana
    form=UserForm()
    user = User.query.get(user_id)
    form.name.data = user.name
    form.username.data = user.username

    return render_template("auth/updateuser.html", form = form, user_id = user_id)

@app.route("/auth/<user_id>/", methods=["POST"])
@login_required(role="ANY")
def user_confirmupdate(user_id):

    user = User.query.get(user_id)
    form = UserForm(request.form)
    
    if not form.validate():
        return render_template("auth/updateuser.html", form = form, user_id=user_id)

    alreadyExistsUser = User.query.filter_by(username=form.username.data).first()
    
    # Tarkistetaan muokkauksessa ettei samannimistä käyttäjää ole, oma olemassaoleva käyttäjätunnus käy
    if alreadyExistsUser and current_user != alreadyExistsUser:
        form.username.errors.append("käyttäjätunnus on jo olemassa, valitse toinen käyttäjätunnus")
        return render_template("auth/updateuser.html", form = form, user_id=user_id)

    # Salasanan salaus
    pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

    user.name = form.name.data
    user.username =form.username.data
    user.password = pw_hash
    
    db.session().commit()

    children = Child.query.filter(Child.account_id == user_id)

    return render_template("auth/showuser.html", children=children, user = user)