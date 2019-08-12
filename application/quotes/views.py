from application import app, db
from flask import redirect, render_template, request, url_for
from application.quotes.models import Quote
from application.quotes.forms import QuoteForm
from flask_login import login_required
from application.child.models import Child

#@app.route("/auth", methods=["GET"])
#def user_index():
    #childrencount = User.how_many_children()
    #return render_template("auth/userlist.html", childrencount = childrencount)

@app.route("/quotes", methods=["GET"])
def quotes_index():
    list = Quote.quotes_with_names()
    return render_template("quotes/list.html", quotes = Quote.query.all(), list=list)

@app.route("/child/quotes/list/<child_id>", methods=["POST","GET"])
@login_required
def quotes_childquotes(child_id):
    return render_template("quotes/ownquoteslist.html", find_child_quotes = Quote.find_child_quotes, child_id = child_id)    

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
@app.route("/child/quotes/modifyState/<quote_id>", methods=["GET", "POST"])
@login_required
def quotes_modifyState(quote_id):

    return render_template("quotes/modifystate.html",quote_id = quote_id)

@app.route("/child/quotes/<quote_id>", methods=["POST"])
@login_required
def quotes_update(quote_id):

    quote = Quote.query.get(quote_id)
    form = QuoteForm(request.form)
    quote.quote = form.name.data
    

    db.session().commit()

    return redirect(url_for("quotes_index"))

#@app.route("/quotes/<child_id>/list", methods=["GET"])
#def quotes_ownquotes():
    #return render_template("quotes/list.html", quotes = Quote.query.all())
 
