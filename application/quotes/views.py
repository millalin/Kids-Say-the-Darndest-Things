from application import app, db
from flask import redirect, render_template, request, url_for
from application.quotes.models import Quote
from application.quotes.forms import QuoteForm


@app.route("/quotes", methods=["GET"])
def quotes_index():
    return render_template("quotes/list.html", quotes = Quote.query.all())

@app.route("/quotes/new/")
def quotes_form():
    return render_template("quotes/new.html", form = QuoteForm())

@app.route("/quotes/", methods=["POST"])
def quotes_create():
    form = QuoteForm(request.form)

    if not form.validate():
        return render_template("quotes/new.html", form = form)

    q = Quote(form.name.data)

    db.session.add(q)
    db.session().commit()
  
    return  redirect(url_for("quotes_index"))

# sivun haku kun sanontaa halutaan muokata
@app.route("/quotes/modifyState/<quote_id>/", methods=["GET", "POST"])
def quotes_modifyState(quote_id):

    return render_template("quotes/modifystate.html", quote_id = quote_id)

@app.route("/quotes/<quote_id>/", methods=["POST"])
def quotes_update(quote_id):

    quote = Quote.query.get(quote_id)
    q = Quote(request.form.get("quote"))
    
    quote.quote = q.quote
    
    db.session().commit()

    return redirect(url_for("quotes_index"))
