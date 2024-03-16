from config.database_config import db, Database_Config

class Expenses_Model(db.Model):
    __bind_key__ = 'db1'
    expenses_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer) #, db.ForeignKey('user.id')
    share_amount = db.Column(db.Float, default=None)
    receipt_id = db.Column(db.Integer)
    __tablename__ = 'expenses'
