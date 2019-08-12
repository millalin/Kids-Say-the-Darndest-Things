from application import db
from application.models import Base

class Quote(Base):
  
    quote = db.Column(db.String(2000), nullable=False)

    child_id = db.Column(db.Integer, db.ForeignKey('child.id'),
                           nullable=False)
    
    def __init__(self, quote):
        self.quote = quote