from flask import jsonify, request
from config.database_config import db
from model.currencies_model import Currencies_Model
from model.expenses_model import Expenses_Model
from model.currency_conversion_model import Currency_Conversion_Model
import json
import base64
from currency_converter import CurrencyConverter
from decimal import Decimal, ROUND_HALF_UP
import requests

class Currency_Utility:
    #def __init__(self):

    def currency_converter_expense(self, data):
        try:
            if 'amount' not in data or 'from_currency' not in data or 'to_currency' not in data:
                return jsonify(message='Invalid request. Please provide amount, from_currency, and to_currency.'), 400

            c = CurrencyConverter()
            amount = data['amount']
            from_currency = data['from_currency']
            to_currency = data['to_currency']
            converted_amount = c.convert(float(amount), from_currency, to_currency)
            exchange_rate = converted_amount/float(amount)
            converted_amount = round(converted_amount, 2)
            
            return jsonify(converted_amount=converted_amount, exchange_rate = exchange_rate)

        except requests.exceptions.RequestException as e:
            return jsonify(message=f'Error connecting to the currency conversion service: {str(e)}'), 500

        except Exception as e:
            return jsonify(message=f'Error converting currency: {str(e)}'), 500
        
    def read_all_currencies(self, data=None):
        try:
            if not bool(data):
                currencies = Currencies_Model.query.all()
                if currencies:
                    currency_list = [{'currency_id': currency.currency_id, 'code': currency.code, 'name': currency.name} for currency in currencies]
                    return jsonify(currency=currency_list, status_code = '200')
                else:
                    return jsonify(message=f'Currencies are not found', status_code = '404'), 404
            else:
                currencies_id = data.get('currencyId')
                currencies = db.session.get(Currencies_Model, currencies_id)
                if currencies:
                    return jsonify(currency_id=currencies.currency_id, code=currencies.code, name=currencies.name, status_code = '200')
        except Exception as e:
            return jsonify(message=f'Error read currencies: {str(e)}', status_code = '500'), 500
        
    def create_currency_converter(self, data):
        try:
            if "expense_id" not in data:
                return jsonify(message='Invalid request. Please provide expense id.', status_code = 400), 400
            else:
                expenses = Expenses_Model.query.filter_by(expenses_id=data['expense_id']).all()
                if not expenses:
                    return jsonify(message='Invalid request. Please provide valid expenses id.', status_code=400), 400
            if "original_currency" not in data:
                return jsonify(message='Invalid request. Please provide original currency.', status_code = 400), 400
            else:
                currency = Currencies_Model.query.filter_by(currency_id=data['original_currency']).all()
                if not currency:
                    return jsonify(message='Invalid request. Please provide valid orginal currency id.', status_code=400), 400
            if "convert_currency" not in data:
                return jsonify(message='Invalid request. Please provide convert currency.', status_code = 400), 400
            else:
                currency = Currencies_Model.query.filter_by(currency_id=data['convert_currency']).all()
                if not currency:
                    return jsonify(message='Invalid request. Please provide valid convert currency id.', status_code=400), 400
            if "exchange_rate" not in data:
                return jsonify(message='Invalid request. Please provide exchange rate.', status_code = 400), 400
            if "converted_amount" not in data:
                return jsonify(message='Invalid request. Please provide converted amount.', status_code = 400), 400
            
            data['converted_amount'] = round(float(data['converted_amount']), 2)

            new_converted_currency = Currency_Conversion_Model(expense_id = data['expense_id'], 
                                                               original_currency = data['original_currency'],
                                                               convert_currency = data['convert_currency'],
                                                               exchange_rate = data['exchange_rate'],
                                                               converted_amount = data['converted_amount']
                                                            )
            db.session.add(new_converted_currency)

            if "commit" not in data:
                db.session.commit()
            
            return jsonify(message='Currency Converter created successfully!', status_code = 200), 200

        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify(message=f'Error creating currency converter: {str(e)}', status_code = 500), 500