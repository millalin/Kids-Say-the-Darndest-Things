from application import app, db, login_required
from flask import redirect, render_template, request, url_for
from application.category.models import Category
from application.category.forms import CategoryForm
from flask_login import current_user


@app.route("/category", methods=["GET"])
@login_required(role="ANY")
def category_index():
    return render_template("category/listcategory.html", c = Category.query.all())

@app.route("/category/newcategory/")
@login_required(role="ANY")
def category_form():
    return render_template("category/newcategory.html", form = CategoryForm())

@app.route("/category/", methods=["GET","POST"])
@login_required(role="ADMIN")
def category_create():
    form = CategoryForm(request.form)

    if not form.validate():
        return render_template("category/newcategory.html", form = form)

    c = Category(name = form.name.data)

    db.session.add(c)
    db.session().commit()
  
    return  redirect(url_for("category_index"))

@app.route("/category/updatecategory/<category_id>/", methods=["GET", "POST"])
@login_required(role="ADMIN")
def category_update_category(category_id):
    # Asetetaan lomakkeelle valmiiksi olemassaolevat tiedot
    form=CategoryForm()
    c = Category.query.get(category_id)
    form.name.data = c.name
    
    return render_template("category/show_update_category.html", form = form, category_id=category_id, c=c)

@app.route("/category/update/<category_id>", methods=["GET","POST"])
@login_required(role="ADMIN")
def category_update(category_id):
    form = CategoryForm(request.form)

    c = Category.query.get(category_id)
    if not form.validate():
        return render_template("category/show_update_category.html", form = form,c=c, category_id=category_id)

    c.name = form.name.data

    db.session().commit()
  
    return  redirect(url_for("category_index"))

@app.route("/category/delete/<category_id>", methods=["GET","POST"])
@login_required(role="ADMIN")
def category_delete(category_id):
    
    category = Category.query.get(category_id)
    
    db.session.delete(category)
    db.session().commit()
    
    return redirect(url_for("category_index"))