from flask import jsonify, request
from config.database_config import db
from utility.user_utility import User_Utility
from utility.groups_utility import Groups_Utility
from utility.grouping_utility import Grouping_Utility
from utility.friends_utility import Friends_Utility

class User_Controller:
    def __init__(self, app):
        self.app = app
        self.user_utility = User_Utility()

        @app.route('/profile/<userID>', methods=["GET"])
        def get_profile(userID):
            # Get profile data
            user_db = User_Utility()
            user, user_status_code = user_db.get(user_id=userID)
            if not isinstance(user, dict):
                return jsonify(message=user), user_status_code

            # Get friends data
            friends_db = Friends_Utility()
            friend_ids, _ = friends_db.list_friend_ids_by_user_id(user_id=user.get('user_id'))
            friends, friends_status_code = user_db.list_by_user_ids(friend_ids)
            if not isinstance(friends, list):
                return jsonify(message=friends), friends_status_code

            # Get grouping data
            groups = []
            groups_db = Groups_Utility()
            grouping_db = Grouping_Utility()
            group_ids, group_ids_status_code = grouping_db.list_group_ids_by_user_id(user_id=userID)
            if not isinstance(group_ids, list):
                return jsonify(message=group_ids), group_ids_status_code
            
            for id in group_ids:
                member_ids, member_ids_status_code = grouping_db.list_user_ids_by_group_id(group_id=id)
                if not isinstance(member_ids, list):
                    return jsonify(message=member_ids), member_ids_status_code
                
                members = []
                for userID in member_ids:
                    member, member_status_code = user_db.get(user_id=userID)
                    if not isinstance(member, dict):
                        return jsonify(message=member), member_status_code
                    members.append(member)

                group_name = groups_db.get(group_id=id)
                groups.append({'members': members, 'name': group_name})

            return jsonify(user=user, friends=friends, groups=groups), 200
        
        @app.route('/user/<userID>', methods=["PUT"])
        def update_profile(userID):
            data = request.get_json()
            user_details = data.get('user_details')

            user_db = User_Utility()
            user, user_status_code = user_db.update(
                user_id=userID, 
                first_name=user_details.get('first_name'),
                last_name=user_details.get('last_name'),
                user_name=user_details.get('user_name'),
                bio=user_details.get('bio'),
            )
            if not isinstance(user, dict):
                return jsonify(message=user), user_status_code
            
            return jsonify(user=user), user_status_code


        @app.route('/user/readUser', methods=['POST'])
        def read_user():
            data = request.get_json()
            return self.user_utility.read_user(data)
        
        @app.route('/user/login', methods=['POST'])
        def login():
            data = request.get_json()
            return self.user_utility.login(data)
        
        @app.route('/user/forgotPassword', methods=['POST'])
        def forgot_password():
            data = request.get_json()
            return self.user_utility.forgot_password(data)
        
        @app.route('/user/changePassword', methods=['POST'])
        def change_password():
            data = request.get_json()
            return self.user_utility.change_password(data)