from flask_wtf import FlaskForm
from wtforms import StringField, DateField, validators, SelectField, ValidationError
from datetime import date


class ChildForm(FlaskForm):
    name = StringField("Lapsen nimi", [validators.Length(min=2, max=30, message="Nimen tulee olla 2-30 merkkiä pitkä")])
    birthday = DateField("Lapsen syntymäpäivä", [validators.DataRequired (message="Kirjoita syntymäpäivä muodossa yyyy-mm-dd")])


    class Meta:
        csrf = False

class MakeSureForm(FlaskForm):
    name = StringField("Oletko varma, että haluat poistaa tämän lapsen? Toiminto poistaa pysyvästi myös lapsen kaikki sanonnat. Vahvistaaksesi poiston, kirjoita x ja paina 'Poista'")

    class Meta:
        csrf = False

class ChildSelectForm(FlaskForm):

    selection = SelectField('Valitse lapsi:', [validators.DataRequired('Valitse yksi lapsi')],coerce=str)

    class Meta:
        csrf = False