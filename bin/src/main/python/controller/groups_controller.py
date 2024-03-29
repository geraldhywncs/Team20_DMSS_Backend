from flask import Flask, jsonify, request
from config.database_config import db
from model.groups_model import Groups_Model
from utility.groups_utility import Groups_Utility

class Groups_Controller:
    def __init__(self, app):
        self.app = app
        self.groups_utility = Groups_Utility()
        with app.app_context():
            db.create_all()
        
            
        # @app.route('/groups/create', methods=['POST'])
        # def create_group():
        #     data = request.get_json()
        #     return self.groups_utility.create_group(data)

        @app.route('/groups/read', methods=['POST'])
        def read_groups():
            data = request.get_json()
            return self.groups_utility.read_groups(data)

        # @app.route('/groups/update', methods=['POST'])
        # def update_group():
        #     data = request.get_json()
        #     return self.groups_utility.update_group(data)
                

        # @app.route('/groups/delete', methods=['POST'])
        # def delete_group():
        #     data = request.get_json()
        #     return self.groups_utility.delete_group(data)
