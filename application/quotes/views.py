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
  
    return  redirect(url_for("quotes_index", child_id = child_id))

# sivun haku kun sanontaa halutaan muokata
@app.route("/quotes/modifyState/<quote_id>", methods=["GET", "POST"])
@login_required
def quotes_modifyState(quote_id):

    return render_template("quotes/modifystate.html", quote_id = quote_id)

@app.route("/quotes/<quote_id>", methods=["POST", "GET"])
@login_required
def quotes_update(quote_id):

    quote = Quote.query.get(quote_id)
    #q = Quote(request.form.get("quote"))
    form = QuoteForm(request.form)
    
    quote.quote = form.name.data
    
    
    
    db.session().commit()

    return redirect(url_for("quotes_index"))
