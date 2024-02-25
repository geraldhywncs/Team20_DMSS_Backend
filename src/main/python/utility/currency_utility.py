from flask import jsonify, request
from config.database_config import db
from model.currencies_model import Currencies_Model
from model.currency_conversion_model import Currency_Conversion_Model
import json
import base64
from forex_python.converter import CurrencyRates
from decimal import Decimal, ROUND_HALF_UP
import requests

class Currency_Utility:
    #def __init__(self):

    def currency_converter_expense(self, data):
        try:
            if 'amount' not in data or 'from_currency' not in data or 'to_currency' not in data:
                return jsonify(message='Invalid request. Please provide amount, from_currency, and to_currency.'), 400

            c = CurrencyRates()
            amount = data['amount']
            from_currency = data['from_currency']
            to_currency = data['to_currency']
            
            exchange_rate = c.get_rate(from_currency, to_currency)
            converted_amount = round(float(amount) * float(exchange_rate), 2)
            
            return jsonify(converted_amount=converted_amount, exchange_rate = exchange_rate)

        except requests.exceptions.RequestException as e:
            return jsonify(message=f'Error connecting to the currency conversion service: {str(e)}'), 500

        except Exception as e:
            return jsonify(message=f'Error converting currency: {str(e)}'), 500
        
    def read_all_currencies(self, data=None):
        try:
            if data is None:
                currencies = Currencies_Model.query.all()
                if currencies:
                    currency_list = [{'currency_id': currency.currency_id, 'code': currency.code, 'name': currency.name} for currency in currencies]
                    return jsonify(currency=currency_list)
                else:
                    return jsonify(message=f'Currencies are not found'), 404
            else:
                currencies_id = data.get('currencyId')
                currencies = Currencies_Model.query.get(currencies_id)
                if currencies:
                    return jsonify(currency_id=currencies.currency_id, code=currencies.code, name=currencies.name)
        except Exception as e:
            return jsonify(message=f'Error read currencies: {str(e)}'), 500
        
    def create_currency_converter(self, data):
        try:
            if "expense_id" not in data:
                return jsonify(message='Invalid request. Please provide expense id.'), 400
            if "original_currency" not in data:
                return jsonify(message='Invalid request. Please provide original currency.'), 400
            if "convert_currency" not in data:
                return jsonify(message='Invalid request. Please provide convert currency.'), 400
            if "exchange_rate" not in data:
                return jsonify(message='Invalid request. Please provide exchange rate.'), 400
            if "converted_amount" not in data:
                return jsonify(message='Invalid request. Please provide converted amount.'), 400
            
            new_converted_currency = Currency_Conversion_Model(expense_id = data['expense_id'], 
                                                               original_currency = data['original_currency'],
                                                               convert_currency = data['convert_currency'],
                                                               exchange_rate = data['exchange_rate'],
                                                               converted_amount = data['converted_amount']
                                                            )
            db.session.add(new_converted_currency)
            db.session.commit()
            return jsonify(message='Currency Converter created successfully!')
        except Exception as e:
            return jsonify(message=f'Error creating currency converter: {str(e)}'), 500