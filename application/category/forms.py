from flask_wtf import FlaskForm
from wtforms import StringField, validators

class CategoryForm(FlaskForm):
    name = StringField("Kategorian nimi", [validators.Length(min=2, message="Kategorian nimen tulee olla vähintään 2 merkkiä pitkä")])
    
 
    class Meta:
        csrf = False
