from application import app, db, login_required
from flask import redirect, render_template, request, url_for
from application.quotes.models import Quote
from application.quotes.forms import QuoteForm
from application.category.forms import CategorySelectForm

from application.child.models import Child
from application.likes.models import Likes
from application.category.models import Category
from flask_login import current_user


@app.route("/quotes", methods=["GET"])
def quotes_index():
    
    list=Quote.quotes_with_names()
        
    return render_template("quotes/list.html", list=list, Quote=Quote)

@app.route("/quotes/bycategory/", methods=["POST", "GET"])
def quotes_get():
    cates=Category.query.all()
    c_list=[(i.name,i.name) for i in cates]
    form = CategorySelectForm()
    form.selection.choices = c_list

    return render_template("quotes/selectcategory.html", form = form)

@app.route("/quotes/bycategory/list", methods=["GET", "POST"])
def quotes_by():
    form=CategorySelectForm()
    name=form.selection.data
    
    category = Category.findCategory(name)
    category_id=category.getId()

    list = Quote.quotes_of_category(category_id)
    return render_template("quotes/listbycategory.html", list=list, name=name)

@app.route("/quotes/list/<child_id>", methods=["POST","GET"])
@login_required(role="ANY")
def quotes_childquotes(child_id):
    child = Child.query.get(child_id)
    name = child.name
    return render_template("quotes/ownquoteslist.html", find_child_quotes = Quote.find_child_quotes, child_id = child_id, name=name)    

@app.route("/quotes/new/<child_id>", methods=["POST", "GET"])
@login_required(role="ANY")
def quotes_form(child_id):
    cates=Category.query.all()
    
   
    c_list=[(i.name,i.name) for i in cates]
    
    form = QuoteForm()
    form.categories.choices = c_list

    return render_template("quotes/new.html", form = form, child_id=child_id)

@app.route("/quotes/new/create/<child_id>", methods=["POST", "GET"])
@login_required(role="ANY")
def quotes_create(child_id):
    
    form = QuoteForm(request.form)
 
    cates=Category.query.all()
    c_list=[(i.name,i.name) for i in cates]
        
    form = QuoteForm()
    form.categories.choices = c_list

    if not form.validate():
        
        return render_template("quotes/new.html", form = form, child_id=child_id)

        
    q = Quote(quote = form.name.data, agesaid = form.age.data, child_id = child_id)

    allcategories=form.categories.data

    for category in  allcategories:
       
        c = Category.findCategory(category)
       
        q.quotecategory.append(c)     

    db.session.add(q)
    db.session().commit()
  
    return redirect(url_for("quotes_childquotes", child_id=child_id))

# sivun haku kun sanontaa halutaan muokata
@app.route("/quotes/modifyState/<quote_id>/<child_id>", methods=["GET", "POST"])
@login_required(role="ANY")
def quotes_modifyState(quote_id, child_id):

    cates=db.session.query(Category).all()
    c_list=[(i.name,i.name) for i in cates]
    
    
    form = QuoteForm()
    
    form.categories.choices = c_list
    
    return render_template("quotes/modifystate.html",form = form, quote_id = quote_id, child_id=child_id)

@app.route("/quotes/<quote_id>/<child_id>", methods=["POST"])
@login_required(role="ANY")
def quotes_update(quote_id,child_id):

    quote = Quote.query.get(quote_id)
    form = QuoteForm(request.form)

    cates=Category.query.all()
    c_list=[(i.name,i.name) for i in cates]
        
    form = QuoteForm()
    form.categories.choices = c_list
    if not form.validate():
    
        return render_template("quotes/modifystate.html",form = form, quote_id = quote_id,child_id=child_id)


    quote.quote = form.name.data
    quote.agesaid = form.age.data
    
    allcategories=form.categories.data

    for category in  allcategories:
        
        c = Category.findCategory(category)

        quote.quotecategory.append(c)     



    db.session().commit()

    return redirect(url_for("quotes_childquotes", child_id=child_id))

#@app.route("/quotes/<child_id>/list", methods=["GET"])
#def quotes_ownquotes():
    #return render_template("quotes/list.html", quotes = Quote.query.all())

@app.route("/quotes/<quote_id>/del/<child_id>", methods=["GET","POST"])
@login_required(role="ANY")
def quotes_delete(quote_id,child_id):
    
    quote = Quote.query.get(quote_id)
        
        
    db.session.delete(quote)
    db.session().commit()
    
    return redirect(url_for("quotes_childquotes", child_id=child_id))
 
@app.route("/quotes/show/<quote_id>", methods=["GET", "POST"])
@login_required(role="ANY")
def quotes_showOne(quote_id):

    quote = Quote.query.get(quote_id)
    child_id = quote.child_id
    quote_id=quote_id
    return render_template("quotes/showOneQuote.html",categorieslist=Category.findCategories(quote_id),child_id = child_id, quote=quote)

@app.route("/quotes/top", methods=["GET", "POST"])
def quotes_top():

    list=Likes.topliked()
        
    return render_template("quotes/topliked.html", list=list)

