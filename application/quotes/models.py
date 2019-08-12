from application import db
from application.models import Base

from sqlalchemy.sql import text

class Quote(Base):
  
    quote = db.Column(db.String(2000), nullable=False)

    child_id = db.Column(db.Integer, db.ForeignKey('child.id'),
                           nullable=False)
    
    def __init__(self, quote):
        self.quote = quote

    @staticmethod
    def find_child_quotes(child_id):
        stmt = text("SELECT Quote.id, Quote.quote FROM Quote"
                     " WHERE Child_id=:cid"
                     " ORDER BY Quote.id").params(cid = child_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "quote":row[1]})

        return response

    
    @staticmethod
    def quotes_with_names():
        stmt = text("SELECT Quote.id, Quote.quote, Child.name AS n FROM Quote"
                     " JOIN Child ON Child.id = Quote.child_id"
                     " GROUP BY Quote.id")
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1], "n":row[2]})

        return response