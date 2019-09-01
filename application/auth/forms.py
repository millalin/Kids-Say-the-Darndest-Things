from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
from wtforms.widgets import PasswordInput
from wtforms.validators import InputRequired, EqualTo
  
class LoginForm(FlaskForm):
    username = StringField("Käyttäjänimi", [InputRequired()])
    password = PasswordField("Salasana", [InputRequired()])
  
class UserForm(FlaskForm):
    name = StringField("Nimi", [validators.Length(min=2, max=30, message= "Nimen tulee olla 2-30 merkin pituinen" )])
    username = StringField("Käyttäjänimi", [validators.Regexp(r'^[\w.@+-]+$', message = "Kirjoita käyttäjätunnus ilman välilyöntiä"),validators.Length(min=2, max=20, message= "Käyttäjänimen tulee olla 2-20 merkin pituinen" )])
    password = StringField('Salasana', [InputRequired(), validators.Length(min=8), EqualTo('password_again', message='Salasanojen täytyy täsmätä')], widget=PasswordInput(hide_value=False))
    password_again = StringField('Toista salasana', widget=PasswordInput(hide_value=False))

    class Meta:
        csrf = False

class MakeSureFormUser(FlaskForm):
    name = StringField("Oletko varma, että haluat poistaa tämän käyttäjän? Toiminto poistaa pysyvästi käyttäjän kaikki lapset sekä sanonnat. Vahvistaaksesi poiston, kirjoita x ja paina 'Poista'")

    class Meta:
        csrf = False
