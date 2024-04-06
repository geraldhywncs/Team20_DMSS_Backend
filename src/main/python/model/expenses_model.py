from config.database_config import db, Database_Config
from sqlalchemy import DECIMAL

class Expenses_Model(db.Model):
    __bind_key__ = 'db1'
    expenses_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer) #, db.ForeignKey('user.id')
    share_amount = db.Column(DECIMAL(65, 2))
    receipt_id = db.Column(db.Integer)
    __tablename__ = 'expenses'

