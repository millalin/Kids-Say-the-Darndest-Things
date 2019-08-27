from application import app, db, login_required
from flask import redirect, render_template, request, url_for
from application.quotes.models import Quote
from application.likes.models import Likes
from flask_login import current_user





@app.route("/quotes/<page>/<quote_id>/like/", methods=["GET","POST"])
@login_required(role="ANY")
def like_quote(quote_id, page):

    q = Quote.query.get(quote_id)
    u = current_user

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

    Likes.query.filter_by(quote_id=q.id, account_id=u.id).delete()
    l = Likes(account_id=u.id, quote_id=q.id, like_count=0)
    db.session().add(l)
    db.session().commit()


    return redirect(url_for("quotes_index", page=page))