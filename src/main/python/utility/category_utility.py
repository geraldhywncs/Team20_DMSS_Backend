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
        try:
            user_id = data.get('user_id')
            if user_id is not None:
                categories = Category_Model.query.filter_by(user_id=user_id).all()
                if categories:  
                    categories_list = [{'category_id':category.category_id, 'category_name':category.category_name, 'user_id':category.user_id} for category in categories]
                    return jsonify(categories=categories_list, status_code="200")
                else:
                    return jsonify(message=f'Category with user id {user_id} not found', status_code="404"), 404
            else:
                return jsonify(message=f'User id is not provided'), 404
                
        except Exception as e:
            return jsonify(message=f'Error reading category: {str(e)}', status_code="500"), 500