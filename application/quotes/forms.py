from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators

class QuoteForm(FlaskForm):
    name = StringField("Sanonta", [validators.Length(min=5)])
    age = IntegerField("Ikä jolloin sanottu")
 
    class Meta:
        csrf = False
