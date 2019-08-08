from flask_wtf import FlaskForm
from wtforms import StringField, DateField, validators

class ChildForm(FlaskForm):
    name = StringField("Lapsen nimi", [validators.Length(min=2)])
    birthday = DateField("Lapsen syntymäpäivä")
 
    class Meta:
        csrf = False
