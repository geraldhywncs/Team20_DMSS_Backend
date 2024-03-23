from flask import Flask, jsonify, request
from config.database_config import db
from model.grouping_model import Grouping_Model
from utility.grouping_utility import Grouping_Utility

class Grouping_Controller:
    def __init__(self, app):
        self.app = app
        self.grouping_utility = Grouping_Utility()
            
        @app.route('/grouping/read', methods=['POST'])
        def read_grouping():
            data = request.get_json()
            return self.grouping_utility.read_grouping_by_user_id(data)
            
        # @app.route('/grouping/create', methods=['POST'])
        # def create_grouping():
        #     data = request.get_json()
        #     return self.grouping_utility.create_grouping(data)
            
        @app.route('/grouping/countUserGrouping', methods=['POST'])
        def count_number_of_user_in_group():
            data = request.get_json()
            return self.grouping_utility.count_number_of_user_in_group(data)
