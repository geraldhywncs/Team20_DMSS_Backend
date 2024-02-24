from config.database_config import db, Database_Config

class Currencies_Model(db.Model):
    __bind_key__ = 'db1'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3))
    name = db.Column(db.String(255))

    __tablename__ = 'currencies'