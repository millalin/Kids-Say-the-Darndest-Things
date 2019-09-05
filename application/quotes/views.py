from application import app, db, login_required
from flask import redirect, render_template, request, url_for
from application.quotes.models import Quote
from application.quotes.forms import QuoteForm, AgeSelectForm
from application.category.forms import CategorySelectForm
from application.child.forms import ChildSelectForm

from application.child.models import Child
from application.likes.models import Likes
from application.category.models import Category
from flask_login import current_user


@app.route("/quotes/<page>/", methods=["POST", "GET"])
def quotes_index(page):
    
    # Sivutus, lasketaan sanonnat ja tämän perusteella sivutmäärä, parametrinä valmiiksi aina seuraavan ja edellisen sivun tiedot, 5 sanontaa/s
    quotecount = Quote.quotecount()
    count=quotecount.get("total")
    pages=(count/5)
    page_prev=int(page)-1
    page_next=int(page)+1
    get_quotes = int(page) -1

    # Haetaan kyselyllä kaikki sanonnat sekä niihin liittyvät lapsen nimet ja iät 5 kerrallaan (joka sivulle)
    list =Quote.quotes_with_names(get_quotes)
    
    return render_template("quotes/list.html", list=list, Quote=Quote, page =int(page), pages=pages, page_prev=page_prev, page_next=page_next)

@app.route("/quotes/search/", methods=["POST", "GET"])
def quotes_get():
    # Asetetaan lomakkeelle valinnoiksi tällä hetkellä olemassaolevat adminin lisäämät kategoriat kategoriataulusta
    cates=Category.query.all()
    c_list=[(i.name,i.name) for i in cates]
    form1 = CategorySelectForm()
    form1.selection.choices = c_list

    #haetaan toinen lomake ikävalinnalle
    form2 = AgeSelectForm()

    return render_template("quotes/select.html", form1 = form1, form2 = form2)


@app.route("/quotes/bycategory/list", methods=["POST", "GET"])
def quotes_by_category():

    #Otataan talteen kategoria id, jotta voidaan hakea oikean kategorian sanonnat
    form=CategorySelectForm(request.form)
    name=form.selection.data
    
    category = Category.findCategory(name)
    category_id=category.getId()

    return redirect(url_for("quotes_by", page=1, category_id=category_id, name=name))


@app.route("/quotes/bycategory/list/<page>/<category_id>/<name>", methods=["GET", "POST"])
def quotes_by(page, category_id, name):   

    # Sivutus, lasketaan monta sanontaa kategoriaan kuuluu ja sen mukaan sivut
    quotecount = Quote.quotecount_category(category_id)
    count=quotecount.get("total")
    pages=(count/5)
    page_prev=int(page)-1
    page_next=int(page)+1
    get_quotes = int(page) -1

    #haetaan listalle sivulle kuuluvat sanonnat
    list = Quote.quotes_of_category(category_id, get_quotes)
    counts = Quote.quotes_of_category_count(category_id)
    return render_template("quotes/listbycategory.html", list=list, name=name, Quote=Quote, page =int(page), pages=pages, page_prev=page_prev, page_next=page_next, category_id=category_id, counts=counts)


@app.route("/quotes/byage/list", methods=["POST", "GET"])
def quotes_get_by_age():
    form2=AgeSelectForm(request.form)
    # Asetetaan lomakkeelle valinnoiksi tällä hetkellä olemassaolevat adminin lisäämät kategoriat kategoriataulusta
    cates=Category.query.all()
    c_list=[(i.name,i.name) for i in cates]
    form1 = CategorySelectForm()
    form1.selection.choices = c_list    

    if not form2.validate():
        return render_template("quotes/select.html", form2 = form2, form1=form1)

    age=form2.age.data

    return redirect(url_for("quotes_by_age", page=1, age=age))

@app.route("/quotes/byage/list/<page>/<age>", methods=["GET", "POST"])
def quotes_by_age(page, age):

    # Sivutus, lasketaan monta sanontaa iällä on ja sen mukaan sivut
    quotecount = Quote.quotecount_age(age)
    count=quotecount.get("total")
    pages=(count/5)
    page_prev=int(page)-1
    page_next=int(page)+1
    get_quotes = int(page) -1

    # haetaan listalle sivulle kuuluvat sanonnat
    list = Quote.quotes_of_age(age, get_quotes)
    counts = Quote.quotes_of_age_count(age)
    return render_template("quotes/listbyage.html", list=list, Quote=Quote, age=age, page=int(page), pages=pages, page_prev=page_prev, page_next=page_next, counts=counts)



# Lapsen valinta kun lisätään sanonta
@app.route("/quotes/newquote/selection", methods=["GET", "POST"])
@login_required(role="ANY")
def quotes_addquotes_by_child():
    # Asetetaan valintavaihtoehdoiksi käyttäjän omat lapset
    children=Child.query.filter(Child.account_id == current_user.id)
    child_list=[(i.name,i.name) for i in children]
    form = ChildSelectForm()
    form.selection.choices = child_list

    return render_template("quotes/selectchildquote.html", form=form, child_list=child_list)


@app.route("/quotes/bychild/add", methods=["GET", "POST"])
def quotes_add_by_child():

    # Haetaan lapsi, jolle sanonta lisätään ja otetaan id talteen
    form2=ChildSelectForm()
    name=form2.selection.data
    
    child = Child.query.filter_by(name=name).first()
    child_id=child.getId()

    # Haetaan valintalomakkeelle olemassaolevat kategoriat
    cates=Category.query.all()
    c_list=[(i.name,i.name) for i in cates]
    form = QuoteForm()
    form.categories.choices = c_list

    return render_template("quotes/new.html",child_id=child_id, form=form, name=name)

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

    # Haetaan valitut kategoriat ja lisätään ne yksitellen sanonnalle
    allcategories=form.categories.data

    for category in  allcategories:
       
        c = Category.findCategory(category)
       
        q.quotecategory.append(c)     

    db.session.add(q)
    db.session().commit()
  
    return redirect(url_for("quotes_childquotes", child_id=child_id))

# Kun listataan lapsen sanonnat
@app.route("/quotes/list/selection", methods=["GET", "POST"])
@login_required(role="ANY")
def quotes_childquotes_by_child():
    # Asetetaan valintavaihtoehdoiksi käyttäjän omat lapset
    children=Child.query.filter(Child.account_id == current_user.id)
    child_list=[(i.name,i.name) for i in children]
    form = ChildSelectForm()
    form.selection.choices = child_list

    return render_template("quotes/selectchild.html", form=form, child_list=child_list)

@app.route("/quotes/list/bychild", methods=["GET", "POST"])
def quotes_by_child():

    # Haetaan lapsi, jonka sanontoja halutaan nähdä ja otetaan id talteen
    form=ChildSelectForm()
    name=form.selection.data
    
    child = Child.query.filter_by(name=name).first()
    child_id=child.getId()

    return render_template("quotes/ownquoteslist.html", find_child_quotes = Quote.find_child_quotes,child_id=child_id, name=name)

# Lapsen sanontojen listaus, paluu lomakkeelta
@app.route("/quotes/list/<child_id>", methods=["POST","GET"])
@login_required(role="ANY")
def quotes_childquotes(child_id):

    child = Child.query.get(child_id)
    name = child.name
    return render_template("quotes/ownquoteslist.html", find_child_quotes = Quote.find_child_quotes, child_id = child_id, name=name)  
    

# sivun haku kun sanontaa halutaan muokata
@app.route("/quotes/modifyState/<quote_id>/<child_id>", methods=["GET", "POST"])
@login_required(role="ANY")
def quotes_modifyState(quote_id, child_id):

    cates=db.session.query(Category).all()
    c_list=[(i.name,i.name) for i in cates]

    quote = Quote.query.get(quote_id)
    form = QuoteForm()
    
    form.name.data = quote.quote
    form.age.data = quote.agesaid
    form.categories.choices = c_list
    
    return render_template("quotes/modifystate.html",form = form, quote_id = quote_id, child_id=child_id)

@app.route("/quotes/<quote_id>/<child_id>", methods=["POST"])
@login_required(role="ANY")
def quotes_update(quote_id,child_id):

    quote = Quote.query.get(quote_id)
    form = QuoteForm(request.form)

    # Talletetaan lomakkeelle kategoriavalinnat, tarpeen sivun uudelleennäytössä
    cates=Category.query.all()
    c_list=[(i.name,i.name) for i in cates]
    form = QuoteForm()
    form.categories.choices = c_list
    
    if not form.validate():
    
        return render_template("quotes/modifystate.html",form = form, quote_id = quote_id,child_id=child_id)

    quote.quotecategory.clear()
    db.session().commit()    

    quote.quote = form.name.data
    quote.agesaid = form.age.data
    
    allcategories=form.categories.data

    # käydään läpi kaikki valitut kategoriat ja lisätään ne sanonnalle
    for category in  allcategories:
        c = Category.findCategory(category)
        quote.quotecategory.append(c)     

    db.session().commit()

    return redirect(url_for("quotes_childquotes", child_id=child_id))


# Sanonnan poisto
@app.route("/quotes/<quote_id>/del/<child_id>", methods=["GET","POST"])
@login_required(role="ANY")
def quotes_delete(quote_id,child_id):
    
    quote = Quote.query.get(quote_id)

    likes = Likes.query.filter(quote_id==Likes.quote_id)
    for like in likes:
        db.session.delete(like)
                
    db.session.delete(quote)
    db.session().commit()
    
    return redirect(url_for("quotes_childquotes", child_id=child_id))
 
# Yhden sanonnan tietojen näyttäminen
@app.route("/quotes/show/<quote_id>", methods=["GET", "POST"])
@login_required(role="ANY")
def quotes_showOne(quote_id):

    quote = Quote.query.get(quote_id)
    child_id = quote.child_id
    quote_id=quote_id
    return render_template("quotes/showOneQuote.html",categorieslist=Category.findCategories(quote_id),child_id = child_id, quote=quote)

@app.route("/quotes/top", methods=["GET", "POST"])
def quotes_top():

    # Haetaan 10 eniten tykkäystä saadyt sanonnat
    list=Likes.topliked()
        
    return render_template("quotes/topliked.html", list=list)

# Ylläpitäjän sanonnan poisto
@app.route("/quotes/<page>/<quote_id>/del/", methods=["GET","POST"])
@login_required(role="ADMIN")
def quotes_admin_delete(quote_id, page):
    
    quote = Quote.query.get(quote_id)
    likes = Likes.query.filter(quote_id==Likes.quote_id)
    for like in likes:
        db.session.delete(like) 
           
    db.session.delete(quote)
    db.session().commit()
    
    return redirect(url_for("quotes_index", page=page))



