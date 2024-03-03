from config.database_config import db

class Grouping_Model(db.Model):
    __bind_key__ = 'db1'
    grouping_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    group_id = db.Column(db.Integer)

    __tablename__ = 'userGrouping'
