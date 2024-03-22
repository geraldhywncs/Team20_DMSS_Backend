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