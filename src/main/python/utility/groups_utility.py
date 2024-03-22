from flask import Flask, jsonify, request
from config.database_config import db
from model.groups_model import Groups_Model

class Groups_Utility:
        def create(self, group_name):
            try:
                group = Groups_Model(group_name=group_name)
                db.session.add(group)
                db.session.commit()
                return group.to_dict(), 201
            except Exception as e:
                db.session.rollback()
                return f'Error in Groups_Utility.create(): {str(e)}', 500

        def get(self, group_id):
            try:
                group = db.session.get(Groups_Model, group_id)
                if group is not None:
                    return group.to_dict(), 200
                else:
                    return 'Group not found', 404
            except Exception as e:
                return f'Error in Groups_Utility.get(): {str(e)}', 500

            
        def read_groups(self, data):
            try:
                group_id = data.get('group_id')
                if group_id is not None:
                    groups = db.session.get(Groups_Model, group_id)
                    if groups:
                        return jsonify(groups=groups.to_dict(), status_code='200')
                    else:
                        return jsonify(message=f'Group with ID {group_id} not found', status_code='404'), 404
                else:
                    groups = Groups_Model.query.all()
                    group_list = [group.to_dict() for group in groups]
                    return jsonify(groups=group_list, status_code='200')
            except Exception as e:
                return jsonify(message=f'Error reading groups: {str(e)}', status_code='500'), 500

        # def update_group(self, data):
        #     try:
        #         if 'id' not in data:
        #             return jsonify(message='Group ID not specified in the request'), 400

        #         group_id = data['id']
        #         group = Groups_Model.query.get(group_id)

        #         if not group:
        #             return jsonify(message=f'Group with ID {group_id} not found'), 404
        #         group.name = data['name']
        #         db.session.commit()
        #         return jsonify(message='Group updated successfully!')
        #     except Exception as e:
        #         return jsonify(message=f'Error update group: {str(e)}'), 500

        # def delete_group(self, data):
        #     try:
        #         if 'id' not in data:
        #             return jsonify(message='Group ID not specified in the request'), 400

        #         group_id = data['id']
        #         group = Groups_Model.query.get(group_id)
        #         if not group:
        #             return jsonify(message=f'Group with ID {group_id} not found'), 404
        #         db.session.delete(group)
        #         db.session.commit()
        #         return jsonify(message='Group deleted successfully!')
        #     except Exception as e:
        #         return jsonify(message=f'Error delete group: {str(e)}'), 500
