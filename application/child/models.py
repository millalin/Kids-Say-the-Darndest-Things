from application import db

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())
    name = db.Column(db.String(20), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    
    def __init__(self, name, birthday):
        self.name = name
        self.birthday = birthday