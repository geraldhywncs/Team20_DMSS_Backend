from config.database_config import db

class Grouping_Model(db.Model):
    __bind_key__ = 'db1'
    grouping_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    __tablename__ = 'userGrouping'

    def to_dict(self):
        return {
            'id': self.grouping_id, 
            'group_id': self.group_id,
            'user_id': self.user_id
        }