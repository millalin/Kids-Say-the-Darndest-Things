from application import app, db, login_required
from flask import redirect, render_template, request, url_for
from application.quotes.models import Quote
from application.likes.models import Likes
from flask_login import current_user


# Sanonnan tykkäys
@app.route("/quotes/<page>/<quote_id>/like/", methods=["GET","POST"])
@login_required(role="ANY")
def like_quote(quote_id, page):

    q = Quote.query.get(quote_id)
    u = current_user

    # Tykkäyksessä like_countiksi laitetaan 1
    Likes.query.filter_by(quote_id=q.id, account_id=u.id).delete()
    l = Likes(account_id=u.id, quote_id=q.id, like_count=1)
    db.session().add(l)
    db.session().commit()

    return redirect(url_for("quotes_index", page=page))
    
@app.route("/quotes/<page>/<quote_id>/unlike/", methods=["GET","POST"])
@login_required(role="ANY")
def unlike_quote(quote_id, page):

    q = Quote.query.get(quote_id)
    u = current_user

    # Tykkäyksen postossa like_count vaihdetaan nollaksi
    Likes.query.filter_by(quote_id=q.id, account_id=u.id).delete()
    l = Likes(account_id=u.id, quote_id=q.id, like_count=0)
    db.session().add(l)
    db.session().commit()


    return redirect(url_for("quotes_index", page=page))

# Sanonnan tykkäys ikävalinnassa, oma metodi, jotta tykkäyksen jälkeen voidaan ohjata jäämään oikealle sivulle edelleen ikävalintahaussa
@app.route("/quotes/<page>/<quote_id>/like/<age>", methods=["GET","POST"])
@login_required(role="ANY")
def like_quote_agelist(quote_id, page, age):

    q = Quote.query.get(quote_id)
    u = current_user

    # Tykkäyksessä like_countiksi laitetaan 1
    Likes.query.filter_by(quote_id=q.id, account_id=u.id).delete()
    l = Likes(account_id=u.id, quote_id=q.id, like_count=1)
    db.session().add(l)
    db.session().commit()

    return redirect(url_for("quotes_by_age", page=page, age=age))

# Tykkäyksen poisto ikähakuvalinnassa
@app.route("/quotes/<page>/<quote_id>/unlike/<age>", methods=["GET","POST"])
@login_required(role="ANY")
def unlike_quote_agelist(quote_id, page, age):

    q = Quote.query.get(quote_id)
    u = current_user

    # Tykkäyksen postossa like_count vaihdetaan nollaksi
    Likes.query.filter_by(quote_id=q.id, account_id=u.id).delete()
    l = Likes(account_id=u.id, quote_id=q.id, like_count=0)
    db.session().add(l)
    db.session().commit()


    return redirect(url_for("quotes_by_age", page=page, age=age))

# Sanonnan tykkäys ikävalinnassa, oma metodi, jotta tykkäyksen jälkeen voidaan ohjata jäämään oikealle sivulle edelleen haetulla kategorialla
@app.route("/quotes/<page>/<quote_id>/like/<name>/<category_id>", methods=["GET","POST"])
@login_required(role="ANY")
def like_quote_categorylist(quote_id, page, name, category_id):

    q = Quote.query.get(quote_id)
    u = current_user

    # Tykkäyksessä like_countiksi laitetaan 1
    Likes.query.filter_by(quote_id=q.id, account_id=u.id).delete()
    l = Likes(account_id=u.id, quote_id=q.id, like_count=1)
    db.session().add(l)
    db.session().commit()

    return redirect(url_for("quotes_by", page=page, name=name, category_id=category_id))

# Tykkäyksen poisto kun haettuna tietyn kategorian sanonnat
@app.route("/quotes/<page>/<quote_id>/unlike/<name>/<category_id>", methods=["GET","POST"])
@login_required(role="ANY")
def unlike_quote_categorylist(quote_id, page, name, category_id):

    q = Quote.query.get(quote_id)
    u = current_user

    # Tykkäyksen postossa like_count vaihdetaan nollaksi
    Likes.query.filter_by(quote_id=q.id, account_id=u.id).delete()
    l = Likes(account_id=u.id, quote_id=q.id, like_count=0)
    db.session().add(l)
    db.session().commit()


    return redirect(url_for("quotes_by", page=page, name=name, category_id=category_id))