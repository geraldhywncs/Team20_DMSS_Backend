from flask import jsonify, request
from config.database_config import db
from utility.currency_utility import Currency_Utility
from utility.category_utility import Category_Utility

class Category_Controller:
    def __init__(self, app):
        self.app = app
        self.category_utility = Category_Utility()
        with app.app_context():
            db.create_all()

        @app.route('/category/readCategory', methods=['POST'])
        def read_category():
            data = request.get_json()
            return self.category_utility.read_category(data)