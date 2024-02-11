from config.database_config import db

class Expenses_Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    expenses = db.Column(db.Float)

    __tablename__ = 'expenses'
