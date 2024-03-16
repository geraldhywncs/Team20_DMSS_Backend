from config.database_config import db

class Groups_Model(db.Model):
    __bind_key__ = 'db1'
    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255))
    user_id = db.Column(db.Integer)

    __tablename__ = 'groups'
