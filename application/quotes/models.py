from application import db

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())
    quote = db.Column(db.String(2000), nullable=False)
    
    def __init__(self, quote):
        self.quote = quote