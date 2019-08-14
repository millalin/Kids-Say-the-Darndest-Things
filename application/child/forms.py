from flask_wtf import FlaskForm
from wtforms import StringField, DateField, validators

class ChildForm(FlaskForm):
    name = StringField("Lapsen nimi", [validators.Length(min=2, message="Nimen tulee olla vähintään 2 merkkiä pitkä")])
    birthday = DateField("Lapsen syntymäpäivä")
 
    class Meta:
        csrf = False
