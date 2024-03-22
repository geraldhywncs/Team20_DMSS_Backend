from flask import jsonify, request
from config.database_config import db
from utility.icon_utility import Icon_Utility

class Icon_Controller:
    def __init__(self, app):
        self.app = app
        self.recurring_frequency_utility = Icon_Utility()
        
        @app.route('/icon/readAllIcon', methods=['POST'])
        def read_all_icon():
            data = request.get_json()
            return self.recurring_frequency_utility.read_all_icon(data)
        