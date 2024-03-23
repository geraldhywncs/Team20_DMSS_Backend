from config.database_config import db

class Groups_Model(db.Model):
    __bind_key__ = 'db1'
    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255))

    __tablename__ = 'groups'

    def to_dict(self):
        return {
            'group_id': self.group_id, 
            'group_name': self.group_name
        }
