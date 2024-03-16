from flask import jsonify, request
from config.database_config import db
from utility.recurring_frequency_utility import Recurring_Frequency_Utility

class Recurring_Frequency_Controller:
    def __init__(self, app):
        self.app = app
        self.recurring_frequency_utility = Recurring_Frequency_Utility()
        with app.app_context():
            db.create_all()
        
        @app.route('/recurringFrequency/readAllrecurringFrequencies', methods=['POST'])
        def read_all_recurring_frequency():
            data = request.get_json()
            return self.recurring_frequency_utility.read_all_recurring_frequency(data)

        