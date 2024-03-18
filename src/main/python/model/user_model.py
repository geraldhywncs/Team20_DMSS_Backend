from config.database_config import db

class User_Model(db.Model):
    __bind_key__ = 'db1'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    account_status = db.Column(db.String(255))
    # first_name = db.Column(db.String(255))
    # last_name = db.Column(db.String(255))
    # bio = db.Column(db.string(255))

    __tablename__ = 'users'