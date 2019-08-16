from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectMultipleField, TextAreaField, validators, widgets
from application.category.models import Category
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from application import db

class SelectBox(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class QuoteForm(FlaskForm):
    name = TextAreaField("Sanonta", [validators.Length(min=5, message="Sanonnan tulee olla vähintään 5 merkkiä pitkä")])
    age = IntegerField("Ikä jolloin sanottu", [validators.NumberRange(min=0, max=99, message="iän tulee olla väliltä 0-99")])

    categories = SelectBox('Valitse kategoriat, johon sanonta kuuluu:', coerce=str)
 
   
    class Meta:
        csrf = False
