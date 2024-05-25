from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    deposit_amount = db.Column(db.Float, nullable=False)
