from application import app, db
from flask import redirect, render_template, request, url_for
from application.quotes.models import Quote
from application.quotes.forms import QuoteForm
from flask_login import login_required
from application.child.models import Child


@app.route("/quotes", methods=["GET"])
def quotes_index():
    return render_template("quotes/list.html", quotes = Quote.query.all())

@app.route("/quotes/new/<child_id>", methods=["POST", "GET"])
@login_required
def quotes_form(child_id):
    
    return render_template("quotes/new.html", form = QuoteForm(), child_id=child_id)

@app.route("/quotes/<child_id>", methods=["POST", "GET"])
@login_required
def quotes_create(child_id):
    form = QuoteForm(request.form)

    if not form.validate():
        return render_template("quotes/new.html", form = form)

    q = Quote(form.name.data)
    q.child_id = child_id
    

    db.session.add(q)
    db.session().commit()
  
    return  redirect(url_for("quotes_index"))

# sivun haku kun sanontaa halutaan muokata
@app.route("/quotes/modifyState/<child_id>/<quote_id>", methods=["GET", "POST"])
@login_required
def quotes_modifyState(quote_id, child_id):

    return render_template("quotes/modifystate.html",quote_id = quote_id, child_id = child_id)

@app.route("/quotes/<child_id>/<quote_id>", methods=["POST"])
@login_required
def quotes_update(quote_id, child_id):

    quote = Quote.query.get(quote_id)
    form = QuoteForm(request.form)
    quote.quote = form.name.data
    quote.child_id = child_id

    print("hahahahaha"+form.name.data)
    db.session().commit()

    return redirect(url_for("quotes_index"))

#@app.route("/quotes/<child_id>/list", methods=["GET"])
#def quotes_ownquotes():
    #return render_template("quotes/list.html", quotes = Quote.query.all())
 
