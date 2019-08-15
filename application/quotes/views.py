from application import app, db
from flask import redirect, render_template, request, url_for
from application.quotes.models import Quote
from application.quotes.forms import QuoteForm
from flask_login import login_required
from application.child.models import Child
from application.category.models import Category


@app.route("/quotes", methods=["GET"])
def quotes_index():
    
    return render_template("quotes/list.html", list=Quote.quotes_with_names())

@app.route("/child/quotes/list/<child_id>", methods=["POST","GET"])
@login_required
def quotes_childquotes(child_id):
    child = Child.query.get(child_id)
    name = child.name
    return render_template("quotes/ownquoteslist.html", find_child_quotes = Quote.find_child_quotes, child_id = child_id, name=name)    

@app.route("/quotes/new/<child_id>", methods=["POST", "GET"])
@login_required
def quotes_form(child_id):
    available_groups=db.session.query(Category).all()
    
   # my_cate = [(x.id(), x.name()) for x in my_choices]
    groups_list=[(i.id,i.name) for i in available_groups]
    
    
    form = QuoteForm()
    
    form.categories.choices = groups_list

    return render_template("quotes/new.html", form = form, child_id=child_id)

@app.route("/quotes/new/create/<child_id>", methods=["POST", "GET"])
@login_required
def quotes_create(child_id):
    
    form = QuoteForm(request.form)
    

    #pakko valita vähintään yksi kategoria
    
    #if not form.validate or not form.categories.data:
        #return render_template("quotes/new.html", form=form, cate_error= "Sanonnalle täytyy valita vähintään yksi kategoria")

    if not form.categories.data:
        if not form.categories.data:
            form.categories.errors.append("Sanonnalle täytyy valita vähintään yksi kategoria")
        return render_template("quotes/new.html", form = form, categories=form.categories.data,child_id=child_id)    



        
    q = Quote(quote = form.name.data, agesaid = form.age.data)
    #q.agesaid = form.age.data
    q.child_id = child_id

    allcategories=form.categories.data

    for category in  allcategories:
        
        category = Category(category)

        q.quotecategory.append(category)     

    db.session.add(q)
    db.session().commit()
  
    return  redirect(url_for("quotes_index"))

# sivun haku kun sanontaa halutaan muokata
@app.route("/child/quotes/modifyState/<quote_id>", methods=["GET", "POST"])
@login_required
def quotes_modifyState(quote_id):

    return render_template("quotes/modifystate.html",form = QuoteForm(), quote_id = quote_id)

@app.route("/child/quotes/<quote_id>", methods=["POST"])
@login_required
def quotes_update(quote_id):

    quote = Quote.query.get(quote_id)
    form = QuoteForm(request.form)
    quote.quote = form.name.data
    quote.agesaid = form.age.data
    
    allcategories=form.categories.data

    for category in  allcategories:
        
        category = Category(category)

        quote.quotecategory.append(category)     


    db.session().commit()

    return redirect(url_for("quotes_index"))

#@app.route("/quotes/<child_id>/list", methods=["GET"])
#def quotes_ownquotes():
    #return render_template("quotes/list.html", quotes = Quote.query.all())

@app.route("/child/quotes/<quote_id>/del", methods=["GET","POST"])
@login_required
def quotes_delete(quote_id):
    
    quote = Quote.query.get(quote_id)
        
        
    db.session.delete(quote)
    db.session().commit()
    
    return redirect(url_for("quotes_index"))
 
@app.route("/child/quotes/show/<quote_id>", methods=["GET", "POST"])
@login_required
def quotes_showOne(quote_id):

    quote = Quote.query.get(quote_id)
    child_id = quote.child_id
    quote_id=quote_id
    return render_template("quotes/showOneQuote.html",categorieslist=Category.findCategories(quote_id),child_id = child_id, quote=quote)