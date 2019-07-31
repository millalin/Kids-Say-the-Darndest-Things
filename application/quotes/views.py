from application import app, db
from flask import redirect, render_template, request, url_for
from application.quotes.models import Quote


@app.route("/quotes", methods=["GET"])
def quotes_index():
    return render_template("quotes/list.html", quotes = Quote.query.all())

@app.route("/quotes/new/")
def quotes_form():
    return render_template("quotes/new.html")

@app.route("/quotes/", methods=["POST"])
def quotes_create():
    q = Quote(request.form.get("quote"))

    db.session().add(q)
    db.session().commit()
  
    return  redirect(url_for("quotes_index"))
