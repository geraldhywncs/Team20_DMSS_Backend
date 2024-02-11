from config.database_config import db

class Groups_Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    __tablename__ = 'groups'
