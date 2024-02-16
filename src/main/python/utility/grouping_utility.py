from flask import Flask, jsonify, request
from config.database_config import db
from model.grouping_model import Grouping_Model, Grouping_Backend_Model

class Grouping_Utility:

    def read_grouping_by_group_id(self, data):
        try:
            group_id = data.get('groupId')
            if group_id is not None:
                grouping = Grouping_Model.query.filter_by(group_id=group_id).all()
                if grouping:
                    grouping_list = [{'id': group.id, 'user_id': group.user_id, 'group_id': group.group_id} for group in grouping]
                    return jsonify(grouping=grouping_list)
                else:
                    grouping = Grouping_Backend_Model.query.filter_by(group_id=group_id).all()
                    if grouping:
                        grouping_list = [{'id': group.id, 'user_id': group.user_id, 'group_id': group.group_id} for group in grouping]
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
            new_grouping1 = Grouping_Backend_Model(user_id=data['user_id'], group_id=data['group_id'])
            db.session.add(new_grouping)
            db.session.add(new_grouping1)
            db.session.commit()
            return jsonify(message='Grouping created successfully!')
        except Exception as e:
            return jsonify(message=f'Error creating grouping: {str(e)}'), 500