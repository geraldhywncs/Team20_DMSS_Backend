from config.database_config import db

class Receipt_Model(db.Model):
    __bind_key__ = 'db1'
    receipt_id = db.Column(db.Integer, primary_key=True)
    created_user_id = db.Column(db.Integer) #, db.ForeignKey('user.id')
    title = db.Column(db.String(255))
    description = db.Column(db.String(4000), default=None)
    created_datetime = db.Column(db.DateTime)
    group_id = db.Column(db.Integer, default=None) #, db.ForeignKey('group.id')
    recur_id = db.Column(db.Integer) #, db.ForeignKey('recurring_frequency.id')
    cat_id = db.Column(db.Integer) #, db.ForeignKey('category.id')
    icon_id = db.Column(db.Integer) #, db.ForeignKey('icon.id')
    updated_recur_datetime = db.Column(db.DateTime)

    __tablename__ = 'receipt'

    
