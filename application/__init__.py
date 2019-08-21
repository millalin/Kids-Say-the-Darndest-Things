from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

import os
import psycopg2


if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quotes.db"    
    app.config["SQLALCHEMY_ECHO"] = True

  
db = SQLAlchemy(app)

# kirjautuminen
from application.auth.models import User, current_user
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Ole hyvä ja kirjaudu, jotta voit käyttää toimintoa."

# roolit
from functools import wraps

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user:
                return login_manager.unauthorized()

            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            
            unauthorized = False

            if role != "ANY":
                unauthorized = True
                
            if current_user.get_role() == "ADMIN":
                unauthorized = False

            if current_user.get_role == "USER":
                unauthorized = False

            if current_user.get_role() == role:
                unauthorized = False
              


            if unauthorized:
                return login_manager.unauthorized()
            
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

from application import views

from application.quotes import models
from application.quotes import views

from application.auth import models
from application.auth import views

from application.child import models
from application.child import views

from application.category import models
from application.category import views

from application.likes import models
from application.likes import views


# login toimintoa
from application.auth.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


try: 
    db.create_all()
except:
    pass