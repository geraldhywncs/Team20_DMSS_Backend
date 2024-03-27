from flask import jsonify, request
from utility.groups_utility import Groups_Utility
from utility.grouping_utility import Grouping_Utility
from utility.user_utility import User_Utility

class Groups_Controller:
    def __init__(self, app):
        self.app = app
        self.groups_utility = Groups_Utility()

        @app.route('/groups/<userID>', methods=["GET"])
        def get_groups(userID):
            grouping_db = Grouping_Utility()
            groupings, grouping_status_code = grouping_db.list_by_user_id(userID)
            if not isinstance(groupings, list):
                return jsonify(message=groupings), grouping_status_code
            
            groups = []

            group_db = Groups_Utility()
            user_db = User_Utility()
            for grouping in groupings:
                group, group_status_code = group_db.get(group_id=grouping.get('group_id'))
                if not isinstance(group, dict):
                    return jsonify(message=group), group_status_code

                member_ids, member_ids_status_code = grouping_db.list_user_ids_by_group_id(group_id=grouping.get('group_id'))
                if not isinstance(member_ids, list):
                    return jsonify(message=member_ids), member_ids_status_code
                
                members = []

                for id in member_ids:
                    user, user_status_code = user_db.get(user_id=id)
                    if not isinstance(user, dict):
                        return jsonify(message=user), user_status_code
                    members.append(user.get('user_name'))

                groups.append({'group_name': group.get('group_name'), 'members': members})

            return jsonify(groups=groups), 200

        @app.route('/groups', methods=['POST'])
        def create_group():
            data = request.get_json()

            groups_db = Groups_Utility()
            group, group_status_code = groups_db.create(group_name=data.get('group_name'))
            if not isinstance(group, dict):
                return jsonify(message=group), group_status_code
            
            grouping_db = Grouping_Utility()
            user_db = User_Utility()
            group_member_ids = data.get('group_member_ids')
            group_members = []
            for id in group_member_ids:
                grouping, grouping_status_code = grouping_db.create(group_id=group.get('group_id'), user_id=id)
                if not isinstance(grouping, dict):
                    return jsonify(message=grouping), grouping_status_code
                
                user, user_status_code = user_db.get(id)
                if not isinstance(user, dict):
                    return jsonify(message=user), user_status_code
                group_members.append(user)

            return jsonify(group=group, group_members=group_members), 200

        @app.route('/groups/read', methods=['POST'])
        def read_groups():
            data = request.get_json()
            return self.groups_utility.read_groups(data)
