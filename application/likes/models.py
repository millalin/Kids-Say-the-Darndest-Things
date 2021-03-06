from application import db
from application.models import Base
from flask_login import current_user

from sqlalchemy.sql import text

class Likes(Base):
  
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    quote_id = db.Column(db.Integer, db.ForeignKey('quote.id'), nullable=False)
    like_count = db.Column(db.Integer, nullable=False)
    
    
    def __init__(self, like_count, account_id,quote_id):
        self.like_count = like_count
        self.account_id = account_id
        self.quote_id = quote_id
        

    @staticmethod
    def count_likes_for_quote(quote_id):
        stmt = text("SELECT COUNT(like.id) AS total FROM Likes"
                     " WHERE Likes.quote_id=:qid"
                     " AND like_count=1").params(qid = quote_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"total":row[0]})

        return response


    @staticmethod
    def topliked():
        stmt = text(" SELECT quote.id, quote.quote, COUNT(likes.id) AS num FROM likes, quote"
                    " WHERE quote.id=likes.quote_id AND like_count=1" 
                    " GROUP BY like_count, quote.id, quote.quote"
                    " ORDER BY num DESC"
                    " LIMIT 10")

        res = db.engine.execute(stmt)
  
        response = []
        for row in res:
            response.append({ "id":row[0], "name":row[1], "num":row[2]})

        return response