from flask import Flask, jsonify, request
from config.database_config import db
from model.grouping_model import Grouping_Model
from utility.grouping_utility import Grouping_Utility

class Grouping_Controller:
    def __init__(self, app):
        self.app = app
        self.grouping_utility = Grouping_Utility()
        with app.app_context():
            db.create_all()
            
        # @app.route('/grouping/readById', methods=['POST'])
        # def read_grouping():
        #     data = request.get_json()
        #     return self.grouping_utility.read_grouping(data)
            
        @app.route('/grouping/create', methods=['POST'])
        def create_grouping():
            data = request.get_json()
            return self.grouping_utility.create_grouping(data)