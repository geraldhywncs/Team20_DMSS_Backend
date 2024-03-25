from flask import jsonify, request
from utility.groups_utility import Groups_Utility
from utility.grouping_utility import Grouping_Utility

class Groups_Controller:
    def __init__(self, app):
        self.app = app
        self.groups_utility = Groups_Utility()
            
        @app.route('/groups', methods=['POST'])
        def create_group():
            data = request.get_json()

            groups_db = Groups_Utility()
            group, group_status_code = groups_db.create(group_name=data.get('group_name'))
            if not isinstance(group, dict):
                return jsonify(message=group), group_status_code
            
            grouping_db = Grouping_Utility()
            group_member_ids = data.get('group_member_ids')
            for id in group_member_ids:
                grouping, grouping_status_code = grouping_db.create(group_id=group.get('group_id'), user_id=id)
                if not isinstance(grouping, dict):
                    return jsonify(message=grouping), grouping_status_code

            return jsonify(group=group, group_member_ids=group_member_ids), 200

        @app.route('/groups/read', methods=['POST'])
        def read_groups():
            data = request.get_json()
            return self.groups_utility.read_groups(data)
