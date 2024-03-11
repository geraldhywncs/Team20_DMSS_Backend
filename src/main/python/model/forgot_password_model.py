from config.database_config import db

class Reset_Password_Model(db.Model):
    __bind_key__ = 'db1'
    reset_password_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    reset_token = db.Column(db.String(255))

    __tablename__ = 'reset_password'