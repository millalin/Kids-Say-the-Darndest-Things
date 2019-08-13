from application import db
from application.models import Base

from sqlalchemy.sql import text

class Quote(Base):
  
    quote = db.Column(db.String(2000), nullable=False)
    agesaid = db.Column(db.Integer, nullable=False)

    child_id = db.Column(db.Integer, db.ForeignKey('child.id'),
                           nullable=False)
    
    def __init__(self, quote):
        self.quote = quote

    @staticmethod
    def find_child_quotes(child_id):
        stmt = text("SELECT Quote.id, Quote.quote, Quote.agesaid FROM Quote"
                     " WHERE Child_id=:cid"
                     " ORDER BY Quote.id").params(cid = child_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "quote":row[1], "agesaid":row[2]})

        return response

    
    @staticmethod
    def quotes_with_names():
        stmt = text("SELECT Quote.id, Quote.quote, Child.name AS n, Quote.agesaid FROM Quote"
                     " JOIN Child ON Child.id = Quote.child_id"
                     " GROUP BY Quote.id, Child.name")
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1], "n":row[2], "agesaid":row[3]})

        return response