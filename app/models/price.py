from app import db

class Price(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    date = db.Column(db.Date)
    closed_price = db.Column(db.Float)
    stock_id = db.Column(db.Integer,db.ForeignKey("stock.id"))
    stock = db.relationship("Stock",back_populates="prices")

