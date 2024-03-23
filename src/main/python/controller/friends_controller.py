from flask import jsonify, request
from config.database_config import db
from utility.friends_utility import Friends_Utility

class Friends_Controller:
    def __init__(self, app):
        self.app = app
        self.user_utility = Friends_Utility()

        @app.route('/friends/<userID>', methods=["GET"])
        def get_friends(userID):
            friends_db = Friends_Utility()
            friends, friends_status_code = friends_db.list_by_user_id(userID)
            if not isinstance(friends, list):
                return jsonify(message=friends), friends_status_code
            return jsonify(friends=friends), 200
        
        @app.route('/friends/<userID>', methods=["POST"])
        def add_friend(userID):
            data = request.get_json()

            friends_db = Friends_Utility()
            friend, friends_status_code = friends_db.create(user_id=userID, friend_id=data.get('friend_id'))
            if not isinstance(friend, dict):
                return jsonify(message=friend), friends_status_code
            return jsonify(friend=friend), 200
        
        @app.route('/friends/<userID>', methods=["DELETE"])
        def remove_friend(userID):
            data = request.get_json()
            print(data)

            friends_db = Friends_Utility()
            friend, friends_status_code = friends_db.delete(user_id=userID, friend_id=data.get('friend_id'))
            print(friend)
            print(friends_status_code)
            if friends_status_code != 200:
                return jsonify(message=friend), friends_status_code
            return jsonify(message="Successfully removed friend"), 200
