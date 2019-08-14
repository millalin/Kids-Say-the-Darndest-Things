from application import db
from application.models import Base
from flask_login import current_user

from sqlalchemy.sql import text

class Category(Base):
  
    name = db.Column(db.String(20), nullable=False)
    
    
    def __init__(self, name):
        self.name = name
        
    @staticmethod
    def categories_of(qid):
         
        stmt = text("SELECT DISTINCT Category.id, Category.name FROM Category, quotecategory" 
                    " WHERE (quotecategory.quote_id=:q)").params(q=qid)

        #stmt = text("SELECT DISTINCT Category.id, Category.name FROM Category WHERE (Quote.id=:quote)" 
                        #" JOIN quotecatecory on Category.id = quotecategory.category_id"
                        #" JOIN Quote ON quotecategory.quote_id = Quote.id").params(quote=qid)
    
        res = db.engine.execute(stmt)
      
        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1]})
    
        return response