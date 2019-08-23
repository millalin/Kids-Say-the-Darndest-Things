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

  

    # Etsii kategorianimen
    def findCategory(name):   
        if not name:
            return
        
        i = Category.query.filter_by(name=name).first()
            
        return i


        
   