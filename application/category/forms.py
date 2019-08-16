from flask_wtf import FlaskForm
from wtforms import StringField, validators, SelectField

class CategoryForm(FlaskForm):
    name = StringField("Kategorian nimi", [validators.Length(min=2, message="Kategorian nimen tulee olla vähintään 2 merkkiä pitkä")])
    
    class Meta:
        csrf = False
 
class CategorySelectForm(FlaskForm):

    selection = SelectField('Valitse kategoria, jonka sanonnat haluat nähdä:', [validators.DataRequired('Valitse yksi kategoria')],coerce=str)

    class Meta:
        csrf = False
