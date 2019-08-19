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

@app.route("/category/delete/<category_id>", methods=["GET","POST"])
@login_required(role="ADMIN")
def category_delete(category_id):
    
    category = Category.query.get(category_id)
    
    db.session.delete(category)
    db.session().commit()
    
    return redirect(url_for("category_index"))