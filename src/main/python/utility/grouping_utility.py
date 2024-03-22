from flask import Flask, jsonify, request
from config.database_config import db
from model.grouping_model import Grouping_Model
from model.groups_model import Groups_Model
from model.user_model import User_Model
import json
from sqlalchemy.orm import join

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

    def read_grouping_by_user_id(self, data):
        try:
            if "user_id" not in data:
                return jsonify(message=f'User ID is not provided', status_code=400), 400
            else:
                user = User_Model.query.filter_by(user_id=data['user_id']).all()
                if not user:
                    return jsonify(message='Invalid request. Please provide valid user id.', status_code=400), 400
                user_id = data.get('user_id')
                # grouping = Grouping_Model.query.filter_by(user_id=user_id).all()
                joined_query = db.session.query(Groups_Model, Grouping_Model).join(Grouping_Model, Groups_Model.group_id == Grouping_Model.group_id)
                grouping = joined_query.filter(Grouping_Model.user_id == user_id).all()
                print(grouping)
                if grouping:
                    for groups_model, grouping_model in grouping:
                        print(f"Group ID: {groups_model.group_id}")
                        print(f"Group Name: {groups_model.group_name}")
                        print(f"Grouping ID: {grouping_model.grouping_id}")
                        print(f"User ID: {grouping_model.user_id}")
                    grouping_list = [{"grouping_id":grouping_model.grouping_id,"group_id":grouping_model.group_id,"user_id":grouping_model.user_id,"group_name":groups_model.group_name} for groups_model, grouping_model in grouping]
                    return jsonify(grouping=grouping_list, status_code=200), 200
                else:
                    return jsonify(message=f'User with ID {user_id} not found', status_code=400), 400
        except Exception as e:
            return jsonify(message=f'Error reading groups: {str(e)}', status_code=500), 500

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