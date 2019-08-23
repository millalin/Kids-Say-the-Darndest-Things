from application import db
from application.models import Base
from flask_login import current_user

from sqlalchemy.sql import text

class Category(Base):
  
    name = db.Column(db.String(20), nullable=False)
    
    
    def __init__(self, name):
        self.name = name
        
    def getId(self):
        return self.id

    def getName(self):
        return self.name

   

    
    def findCategories(q_id):
        stmt = text("SELECT Category.id, Category.name FROM Category"
                    " JOIN quotecategory ON quotecategory.category_id = Category.id"
                    " WHERE quotecategory.quote_id = :quote_id" ).params(quote_id=q_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1]})

        return response


    # Etsii kategorianimen
    def findCategory(name):   
        if not name:
            return
        
        i = Category.query.filter_by(name=name).first()
            
        return i


        
   