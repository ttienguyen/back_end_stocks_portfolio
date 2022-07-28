from app import db

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    ticker = db.Column(db.String(5))
    shares = db.Column(db.Integer)
    prices = db.relationship("Price", back_populates="stock", lazy=True)