
from config.database_config import db, Database_Config

class Category_Model(db.Model):
    __bind_key__ = 'db1'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255))
    user_id = db.Column(db.Integer)

    __tablename__ = 'category'