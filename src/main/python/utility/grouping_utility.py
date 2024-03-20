from flask import Flask, jsonify, request
from config.database_config import db
from model.grouping_model import Grouping_Model
import json

class Grouping_Utility:

    def list_group_ids_by_user_id(self, user_id):
        try:
            groupings = Grouping_Model.query.filter_by(user_id=user_id).all()
            return [grouping.group_id for grouping in groupings], 200
        except Exception as e:
            return f'Error in Grouping_Utility.list_group_ids_by_user_id(): {str(e)}', 500

    def list_user_ids_by_group_id(self, group_id):
        try:
            groupings = Grouping_Model.query.filter_by(group_id=group_id).all()
            return [grouping.user_id for grouping in groupings], 200
        except Exception as e:
            return f'Error in Grouping_Utility.list_user_ids_by_group_id(): {str(e)}', 500


    def read_grouping_by_group_id(self, data):
        try:
            group_id = data.get('groupId')
            if group_id is not None:
                grouping = Grouping_Model.query.filter_by(group_id=group_id).all()
                if grouping:
                    grouping_list = [group.to_dict() for group in grouping]
                    return jsonify(grouping=grouping_list)
                else:
                    return jsonify(message=f'Group with ID {group_id} not found'), 404
            else:
                return jsonify(message=f'Group ID is not provided'), 404
        except Exception as e:
            return jsonify(message=f'Error reading groups: {str(e)}'), 500

    def create_grouping(self, data):
        try:
            new_grouping = Grouping_Model(user_id=data['user_id'], group_id=data['group_id'])
            db.session.add(new_grouping)
            db.session.commit()
            return jsonify(message='Grouping created successfully!', status_code = 200)
        except Exception as e:
            return jsonify(message=f'Error creating grouping: {str(e)}', status_code = 500)
        
    def count_number_of_user_in_group(self, data):
        try:
            group_id = data.get('group_id')
            if group_id is not None:
                grouping_response = self.read_grouping_by_group_id({"groupId": data['group_id']})
                grouping_response_content = grouping_response.get_data(as_text=True)
                grouping_data = json.loads(grouping_response_content).get("grouping", [])
                return jsonify(total_user=len(grouping_data))
            else:
                return jsonify(message=f'Group ID is not provided', status_code=404), 404
        except Exception as e:
            return jsonify(message=f'Error reading groups: {str(e)}'), 500