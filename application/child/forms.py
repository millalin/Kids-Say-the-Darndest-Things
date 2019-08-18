from flask_wtf import FlaskForm
from wtforms import StringField, DateField, validators

class ChildForm(FlaskForm):
    name = StringField("Lapsen nimi", [validators.Length(min=2, max=30, message="Nimen tulee olla 2-30 merkkiä pitkä")])
    birthday = DateField("Lapsen syntymäpäivä")
 
    class Meta:
        csrf = False
