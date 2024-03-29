from flask import jsonify, request
from config.database_config import db
from utility.currency_utility import Currency_Utility
from utility.category_utility import Category_Utility

class Category_Controller:
    def __init__(self, app):
        self.app = app
        self.category_utility = Category_Utility(app)

        @app.route('/category/readCategory', methods=['POST'])
        def read_category():
            data = request.get_json()
            return self.category_utility.read_category(data)

        @app.route('/category/addCategory', methods=['POST'])
        def add_category():
            data = request.get_json()
            return self.category_utility.add_category(data)

        @app.route('/category/deleteCategory', methods=['POST'])
        def delete_category():
            data = request.get_json()
            return self.category_utility.delete_category(data)
