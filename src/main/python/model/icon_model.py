from config.database_config import db

class Icon_Model(db.Model):
    __bind_key__ = 'db1'
    icon_id = db.Column(db.Integer, primary_key=True)
    icon_name = db.Column(db.String(255))

    __tablename__ = 'icon'