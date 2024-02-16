from config.database_config import db, Database_Config

class Expenses_Model(db.Model):
    __bind_key__ = 'db1'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    expenses = db.Column(db.Float)

    __tablename__ = 'expenses'

class Expenses_Backup_Model(db.Model):
    __bind_key__ = 'db2'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    expenses = db.Column(db.Float)

    __tablename__ = 'expenses'
