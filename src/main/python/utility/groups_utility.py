from flask import Flask, jsonify, request
from config.database_config import db
from model.groups_model import Groups_Model

class Groups_Utility:
            
        def create_group(self, data):
            try:
                new_group = Groups_Model(name=data['name'])
                db.session.add(new_group)
                db.session.commit()
                return jsonify(message='Group created successfully!')
            except Exception as e:
                return jsonify(message=f'Error creating group: {str(e)}'), 500
            
        def read_groups(self, data):
            try:

                group_id = data.get('id')
                if group_id is not None:
                    group = Groups_Model.query.get(group_id)
                    if group:
                        return jsonify(id=group.id, name=group.name)
                    else:
                        return jsonify(message=f'Group with ID {group_id} not found'), 404
                else:
                    groups = Groups_Model.query.all()
                    if groups:
                        group_list = [{'id': group.id, 'name': group.name} for group in groups]
                        return jsonify(groups=group_list)
                    else:
                        return jsonify(message=f'Groups are not found'), 404
            except Exception as e:
                return jsonify(message=f'Error reading groups: {str(e)}'), 500

        def update_group(self, data):
            try:
                if 'id' not in data:
                    return jsonify(message='Group ID not specified in the request'), 400

                group_id = data['id']
                group = Groups_Model.query.get(group_id)

                if not group:
                    return jsonify(message=f'Group with ID {group_id} not found'), 404
                group.name = data['name']
                db.session.commit()
                return jsonify(message='Group updated successfully!')
            except Exception as e:
                return jsonify(message=f'Error update group: {str(e)}'), 500

        def delete_group(self, data):
            try:
                if 'id' not in data:
                    return jsonify(message='Group ID not specified in the request'), 400

                group_id = data['id']
                group = Groups_Model.query.get(group_id)
                if not group:
                    return jsonify(message=f'Group with ID {group_id} not found'), 404
                db.session.delete(group)
                db.session.commit()
                return jsonify(message='Group deleted successfully!')
            except Exception as e:
                return jsonify(message=f'Error delete group: {str(e)}'), 500
