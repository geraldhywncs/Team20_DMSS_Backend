from config.database_config import db

class Recurring_Frequency_Model(db.Model):
    __bind_key__ = 'db1'
    recurring_id = db.Column(db.Integer, primary_key=True)
    recur_name = db.Column(db.String(255))

    __tablename__ = 'recurring_frequency'