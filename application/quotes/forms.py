from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectMultipleField, validators, widgets

class SelectBox(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class QuoteForm(FlaskForm):
    name = StringField("Sanonta", [validators.Length(min=5)])
    age = IntegerField("Ikä jolloin sanottu")
    categories = SelectBox('Valitse kategoriat, johon sanonta kuuluu:', choices=[('hauskat', 'hauskat'), ('suhde', 'suhde'), ('kysymykset', 'kysymykset')])
 
    class Meta:
        csrf = False
