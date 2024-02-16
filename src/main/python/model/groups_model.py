from config.database_config import db

class Groups_Model(db.Model):
    __bind_key__ = 'db1'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    __tablename__ = 'groups'

class Groups_Backend_Model(db.Model):
    __bind_key__ = 'db2'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    __tablename__ = 'groups'
