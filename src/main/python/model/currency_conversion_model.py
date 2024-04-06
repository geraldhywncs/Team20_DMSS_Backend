from config.database_config import db, Database_Config
from sqlalchemy import DECIMAL

class Currency_Conversion_Model(db.Model):
    __bind_key__ = 'db1'
    conversion_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    expense_id = db.Column(db.Integer) #, db.ForeignKey('.id')
    original_currency = db.Column(db.Integer) #, db.ForeignKey('.id')
    convert_currency = db.Column(db.Integer) #, db.ForeignKey('.id')
    exchange_rate = db.Column(db.Float)
    converted_amount = db.Column(DECIMAL(65, 2))

    __tablename__ = 'currency_conversion'
