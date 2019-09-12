from application import app, db
from flask import redirect, render_template, request, url_for, flash
from application.child.models import Child
from application.quotes.models import Quote
from application.likes.models import Likes
from application.child.forms import ChildForm, MakeSureForm
from datetime import datetime, date
from flask_login import login_required, current_user
from datetime import date
from wtforms import ValidationError

@app.route("/child", methods=["GET"])
def child_index():
    return render_template("child/listchild.html", quotes = Child.query.all())

# Käyttäjän omien lapsien haku kyselyllä
@app.route("/child/userlist/", methods=["GET"])
@login_required
def child_userchildren():
    return render_template("child/ownchildren.html", find_users_children = Child.find_users_children())

@app.route("/child/newchild/")
@login_required
def child_form():
    return render_template("child/newchild.html", form = ChildForm())

@app.route("/child/", methods=["GET","POST"])
@login_required
def child_create():
    form = ChildForm(request.form)

    if not form.validate():
        return render_template("child/newchild.html", form = form)

    # Tarkastetaan, ettei käyttäjällä ole samannimistä lasta
    alreadyExistsChild = Child.query.filter_by(name=form.name.data, account_id=current_user.id).first()
    if alreadyExistsChild:
        form.name.errors.append("Sinulla on jo tämänniminen lapsi olemassa.")
        return render_template("child/newchild.html", form = form)


    c = Child(name = form.name.data, birthday = form.birthday.data)
    
    c.account_id = current_user.id

    db.session.add(c)
    db.session().commit()
  
    return  redirect(url_for("child_userchildren"))

@app.route("/child/modifychild/<child_id>/", methods=["GET", "POST"])
@login_required
def child_modifychild(child_id):
    # Asetetaan lomakkeelle valmiiksi olemassaolevat tiedot
    form=ChildForm()
    child = Child.query.get(child_id)
    form.name.data = child.name
    form.birthday.data = child.birthday
    return render_template("child/modifyChild.html", form = form, child_id = child_id)

@app.route("/child/<child_id>/", methods=["POST"])
@login_required
def child_update(child_id):

    child = Child.query.get(child_id)
    form = ChildForm(request.form)
    
    if not form.validate():
        return render_template("child/modifyChild.html", form = form, child_id=child_id)

    # Tarkastetaan, ettei käyttäjällä ole samannimistä lasta
    alreadyExistsChild = Child.query.filter_by(name=form.name.data, account_id=current_user.id).first()
    if alreadyExistsChild and child != alreadyExistsChild:
        form.name.errors.append("Sinulla on jo tämänniminen lapsi olemassa.")
        return render_template("child/modifyChild.html", form = form, child_id=child_id)

    child.name = form.name.data
    child.birthday =form.birthday.data
    
    db.session().commit()

    return redirect(url_for("child_userchildren"))


@app.route("/child/<child_id>/delete", methods=["POST","GET"])
@login_required
def child_delete(child_id):

    # Tarkastuslomake, jottei lasta tule poistettua liian helpolla
    form = MakeSureForm()

    return render_template("child/deletechild.html", form = form, child_id=child_id)

@app.route("/child/<child_id>/del", methods=["POST"])
@login_required
def child_deleteConfirm(child_id):

    form = MakeSureForm(request.form)
    ok = form.name.data
    
    # jos tarkastuslomakkeeseen on syötetty oikea tieto, jolla halutaan varmistaa poisto
    if ok == "x":

        c = Child.query.get(child_id)

        # Etsitään lapsen lapsen sanonnat ja poistataan sanonnat sekä sanonnan tykkäykset
        q = Quote.query.filter(Quote.child_id == child_id)
        for quote in q:
               
            likes = Likes.query.filter(Likes.quote_id==quote.id)
            for like in likes:
                db.session.delete(like)
                db.session().commit()

            db.session.delete(quote)
            db.session().commit()

        # Poistetaan lapsi
        db.session().delete(c)
        db.session().commit()
        flash("Lapsi poistettu onnistuneesti", category="success")
        return redirect(url_for("child_userchildren"))
    
    flash("Lasta ei poistettu", category="warning")
    return redirect(url_for("child_userchildren"))

# Yhden lapsen tietojen näyttäminen
@app.route("/child/showchild/<child_id>")
@login_required
def child_showOne(child_id):
    child = Child.query.get(child_id)
    return render_template("child/showchild.html", child_id=child_id, child=child)