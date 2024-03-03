from flask import jsonify, request
from config.database_config import db
from model.category_model import Category_Model
from utility.grouping_utility import Grouping_Utility
from utility.currency_utility import Currency_Utility
import json
import base64
from forex_python.converter import CurrencyRates
from decimal import Decimal, ROUND_HALF_UP
import requests
import time


class Category_Utility:
    # def __init__(self):

    def read_category(self, data):
        print("read_category")
        try:
            category_id = data.get('category_id')
            if category_id is not None:
                category = Category_Model.query.get(category_id)
                if category:
                    return jsonify(category_id=category.category_id, category_name=category.category_name, user_id=category.user_id, status_code=category.status_code)
                else:
                    return jsonify(message=f'Category with ID {category_id} not found', status_code = 404), 404
            else:
                categories = Category_Model.query.all()
                if categories:
                    categories_list = [{'category_id': category.category_id, 'category_name': category.category_name, 'user_id': category.user_id} for category in categories]
                    return jsonify(categories=categories_list, status_code = 200), 200
                else:
                    return jsonify(message=f'Categories are not found', status_code = 404), 404
        except Exception as e:
            return jsonify(message=f'Error reading category: {str(e)}'), 500