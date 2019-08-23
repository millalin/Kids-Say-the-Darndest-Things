from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
  
class LoginForm(FlaskForm):
    username = StringField("Käyttäjänimi")
    password = PasswordField("Salasana")
  

class UserForm(FlaskForm):
    name = StringField("Nimi", [validators.Length(min=2, max=30, message= "Nimen tulee olla 2-30 merkin pituinen" )])
    username = StringField("Käyttäjänimi", [validators.Regexp(r'^[\w.@+-]+$'),validators.Length(min=2, max=20, message= "Käyttäjänimen tulee olla 2-20 merkin pituinen" )])
    password = PasswordField("Salasana", [validators.Length(min=8, message= "Salasanan tulee olla vähintään 8 merkkiä pitkä" )])

    class Meta:
        csrf = False

class MakeSureFormUser(FlaskForm):
    name = StringField("Oletko varma, että haluat poistaa tämän käyttäjän. Vahvistaaksesi poiston, kirjoita x ja paina nappia")

    class Meta:
        csrf = False
