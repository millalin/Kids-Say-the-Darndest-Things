from application import db
from application.models import Base
from flask_login import current_user

from sqlalchemy.sql import text

class Category(Base):
  
    name = db.Column(db.String(20), nullable=False)
    
    
    def __init__(self, name):
        self.name = name
        