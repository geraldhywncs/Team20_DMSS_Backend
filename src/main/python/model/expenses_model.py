from config.database_config import db, Database_Config

class Expenses_Model(db.Model):
    __bind_key__ = 'db1'
    expenses_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer) #, db.ForeignKey('user.id')
    group_id = db.Column(db.Integer, default=None) #, db.ForeignKey('group.id')
    title = db.Column(db.String(255))
    description = db.Column(db.String(255), default=None)
    cat_id = db.Column(db.Integer) #, db.ForeignKey('category.id')
    recur_expense = db.Column(db.String(255), default=None)
    share_amount = db.Column(db.Float, default=None)
    __tablename__ = 'expenses'
