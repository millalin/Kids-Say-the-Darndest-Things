from application import app, db, login_required
from flask import redirect, render_template, request, url_for
from application.quotes.models import Quote
from application.likes.models import Likes
from flask_login import current_user



@app.route("/quotes/<quote_id>/like", methods=["GET","POST"])
@login_required(role="ANY")
def like_new(quote_id):

    
    q = Quote.query.get(quote_id)
    quote_id = quote_id
    #liked=Likes.users_like(quote_id)

    #if liked == 1:
        #l = "Tykätty sanonnasta"
    #else:
        #l = "Et ole vielä tykännyt sanonnasta"


    return render_template("likes/showlikes.html", quote = q, quote_id=quote_id)

@app.route("/quotes/<quote_id>/like/", methods=["GET","POST"])
@login_required(role="ANY")
def like_quote(quote_id):

    value =1
    q = Quote.query.get(quote_id)
    u = current_user

    Likes.query.filter_by(quote_id=q.id, account_id=u.id).delete()
    l = Likes(account_id=u.id, quote_id=q.id, like_count=1)
    db.session().add(l)
    db.session().commit()

    print("muutettu tämä ja lisätty uusi tykkäys testi 99999999999999999999999988888888888888888444444")
    print(q)



    return redirect(url_for("quotes_index"))
    