from application import db
from application.models import Base
from sqlalchemy.sql import text
from flask_login import current_user


class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    role = db.Column(db.String(20), nullable=False)


    children = db.relationship("Child", backref='account', lazy=True)
    #likes = db.relationship("Like", backref='account', lazy=True)

    def __init__(self, name, username, password, role):
        self.name = name
        self.username = username
        self.password = password
        self.role = role
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_role(self):
        return self.role

    @staticmethod
    def how_many_children():
        stmt = text("SELECT Account.id, Account.username, COUNT(Child.id) AS total FROM Account"
                     " LEFT JOIN Child ON Child.account_id = Account.id"
                     " GROUP BY Account.id")
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "username":row[1], "total":row[2]})

        return response


    @staticmethod
    def usercount():
        stmt = text("SELECT COUNT(Account.id) AS total FROM Account")
                 
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"total":row[0]})

        return response