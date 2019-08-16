from application import db
from application.models import Base

from sqlalchemy.sql import text

#many to many liitostaulu sanonnan ja kategorian välille
quotecategory = db.Table('quotecategory',
    db.Column('quote_id',  db.Integer, db.ForeignKey('quote.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Quote(Base):
  
    quote = db.Column(db.String(2000), nullable=False)
    agesaid = db.Column(db.Integer, nullable=False)

    child_id = db.Column(db.Integer, db.ForeignKey('child.id'),
                           nullable=False)
    
    #many to many riippuvuussuhde, määrittely 
    quotecategory = db.relationship('Category', secondary=quotecategory, lazy='subquery',
        backref=db.backref('quotes', lazy=True))

    def __init__(self, quote, agesaid):
        self.quote = quote
        self.agesaid = agesaid

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

    @staticmethod
    def quotes_of_category(id):
        stmt = text("SELECT Quote.id, Quote.quote, Child.name AS n, Quote.agesaid FROM Quote"
                     " JOIN Child ON Child.id = Quote.child_id"
                     " JOIN quotecategory ON quotecategory.quote_id = Quote.id"
            
                     " WHERE quotecategory.category_id=:c_id"
                     " GROUP BY Quote.id, Child.name").params(c_id = id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1], "n":row[2], "agesaid":row[3]})

        return response