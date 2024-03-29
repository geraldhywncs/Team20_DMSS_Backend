from flask import jsonify, request
from config.database_config import db
from model.expenses_model import Expenses_Model
from controller.grouping_controller import Grouping_Controller
from utility.currency_utility import Currency_Utility

class Currency_Controller:
    def __init__(self, app):
        self.app = app
        self.currency_utility = Currency_Utility()
        with app.app_context():
            db.create_all()
        
        @app.route('/currency/currencyConverter', methods=['POST'])
        def currency_converter_expense():
            data = request.get_json()
            return self.currency_utility.currency_converter_expense(data)
        
        @app.route('/currency/readAllCurrencies', methods=['POST'])
        def read_all_currencies():
            return self.currency_utility.read_all_currencies()
        
        @app.route('/currency/createCurrencyConverter', methods=['POST'])
        def create_currency_converter():
            data = request.get_json()
            return self.currency_utility.create_currency_converter(data)