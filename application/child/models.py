from application import db
from application.models import Base
from flask_login import current_user

from sqlalchemy.sql import text

class Child(Base):
  
    name = db.Column(db.String(20), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)

    quotes = db.relationship("Quote", backref='child', lazy=True)
    
    def __init__(self, name, birthday):
        self.name = name
        self.birthday = birthday

    def get_id(self):
        return self.id

    @staticmethod
    def find_users_children():
        stmt = text("SELECT Child.id, Child.name, Child.birthday FROM Child"
                     " WHERE Account_id=:cuid"
                     " ORDER BY Child.id").params(cuid = current_user.id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1], "birthday":row[2]})

        return response