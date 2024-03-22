from config.database_config import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from model.user_model import User_Model

class Friends_Model(db.Model):
    __bind_key__ = 'db1'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.user_id'))
    friend_id = db.Column(db.Integer, ForeignKey('users.user_id'))

    __tablename__ = 'friends'

    # Define a relationship to the User model
    user = relationship(User_Model, foreign_keys=[user_id])
    friend = relationship(User_Model, foreign_keys=[friend_id])

    def to_dict(self):
        return {
            'id': self.id, 
            'user_id': self.user_id,
            'friend_id': self.friend_id
        }
