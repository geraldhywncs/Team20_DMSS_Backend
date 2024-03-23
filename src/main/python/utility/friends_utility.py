from flask import jsonify
from config.database_config import db
from model.friends_model import Friends_Model



class Friends_Utility:
    def create(self, user_id, friend_id):
        try:
            friendship = Friends_Model(user_id=user_id, friend_id=friend_id)
            db.session.add(friendship)
            db.session.commit()
            return friendship.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return f'Error in Friends_Utility.create(): {str(e)}', 500
        
    def delete(self, user_id, friend_id):
        try:
            friend = Friends_Model.query.filter_by(user_id=user_id, friend_id=friend_id).first()
            if friend is not None:
                db.session.delete(friend)
                db.session.commit()
                return 'Friend successfully deleted', 200
            else: 
                return 'Friend not found', 404
        except Exception as e:
            db.session.rollback()
            return f'Error in Friends_Utility.delete(): {str(e)}', 500

    def list_by_user_id(self, user_id):
        try:
            friendship = Friends_Model.query.filter_by(user_id=user_id).all()
            print(friendship)
            return [f.to_dict() for f in friendship], 200
        except Exception as e:
            return f'Error in Friends_Utility.list_by_user_id(): {str(e)}', 500

    def list_friend_ids_by_user_id(self, user_id):
        try:
            friendship = Friends_Model.query.filter_by(user_id=user_id).all()
            return [f.friend_id for f in friendship], 200
        except Exception as e:
            return f'Error in Friends_Utility.list_friend_ids_by_user_id(): {str(e)}', 500