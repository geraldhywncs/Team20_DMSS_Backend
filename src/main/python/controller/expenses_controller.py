from flask import jsonify, request
from config.database_config import db
from model.expenses_model import Expenses_Model
from controller.grouping_controller import Grouping_Controller
from utility.expenses_utility import Expenses_Utility

class Expenses_Controller:
    def __init__(self, app):
        self.app = app
        self.expenses_utility = Expenses_Utility()
        with app.app_context():
            db.create_all()
        
        @app.route('/expenses/create', methods=['POST'])
        def create_expense():
            data = request.get_json()
            return self.expenses_utility.create_expense(data)

        @app.route('/expenses/read', methods=['POST'])
        def get_expenses():
            data = request.get_json()
            return self.expenses_utility.read_expenses(data)
                

        @app.route('/expenses/update', methods=['POST'])
        def update_expense():
            data = request.get_json()
            return self.expenses_utility.update_expense(data)

        @app.route('/expenses/delete', methods=['POST'])
        def delete_expense():
            data = request.get_json()
            return self.expenses_utility.delete_expense(data)

        
        @app.route('/expenses/splitExpense', methods=['POST'])
        def split_expense():
            data = request.get_json()
            return self.expenses_utility.split_expense(data)
        
        @app.route('/expenses/currencyConverter', methods=['POST'])
        def currency_converter_expense():
            data = request.get_json()
            return self.expenses_utility.currency_converter_expense(data)
        
        @app.route('/expenses/readAllCurrencies', methods=['POST'])
        def read_all_currencies():
            return self.expenses_utility.read_all_currencies()