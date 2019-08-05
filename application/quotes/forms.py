from flask_wtf import FlaskForm
from wtforms import StringField, validators

class QuoteForm(FlaskForm):
    name = StringField("Sanonta", [validators.Length(min=5)])
 
    class Meta:
        csrf = False
