from flask import jsonify, request
from config.database_config import db
from model.expenses_model import Expenses_Model
from model.receipt_model import Receipt_Model
from model.user_model import User_Model
from model.category_model import Category_Model
from model.currencies_model import Currencies_Model
from model.icon_model import Icon_Model
from model.groups_model import Groups_Model
from model.recurring_frequency_model import Recurring_Frequency_Model
from utility.grouping_utility import Grouping_Utility
from utility.currency_utility import Currency_Utility
import json
import base64
from decimal import Decimal, ROUND_HALF_UP
import requests
import time
from datetime import datetime

class Expenses_Utility:
    def __init__(self):
        self.grouping_utility = Grouping_Utility()
        self.currency_utility = Currency_Utility()

    def read_expenses(self, data):
        try:
            user_id = data.get('user_id')
            if user_id is None:
                return jsonify(message='User ID is required'), 400

            receipts = Receipt_Model.query.filter_by(created_user_id=user_id).order_by(Receipt_Model.created_datetime.desc()).all()
            if receipts:
                receipt_list = []
                for receipt in receipts:
                    expenses = Expenses_Model.query.filter_by(user_id=user_id, receipt_id=receipt.receipt_id).all()
                    expense_data = [{
                        'expense_id': expense.expenses_id,
                        'share_amount': expense.share_amount
                    } for expense in expenses]

                    category = Category_Model.query.filter_by(user_id=user_id, category_id=receipt.cat_id).first()
                    category_name = category.category_name if category else None

                    recurring = Recurring_Frequency_Model.query.filter_by(recurring_id=receipt.recur_id).first()
                    recurring_name = recurring.recur_name if recurring else None

                    receipt_data = {
                        'receipt_id': receipt.receipt_id,
                        'title': receipt.title,
                        'description': receipt.description,
                        'created_datetime': receipt.created_datetime,
                        'group_id': receipt.group_id,
                        'recur_id': receipt.recur_id,
                        'cat_id': receipt.cat_id,
                        'icon_id': receipt.icon_id,
                        'updated_recur_datetime': receipt.updated_recur_datetime,
                        'category_name': category_name,
                        'recurring_name': recurring_name,
                        'expenses': expense_data  
                    }
                    receipt_list.append(receipt_data)
                return jsonify(receipts=receipt_list)
            else:
                return jsonify(message=f'No receipts found for user with ID {user_id}'), 404
                    
        except Exception as e:
            return jsonify(message=f'Error reading receipts: {str(e)}'), 500

    def read_receipts_by_user(self, data):
        try:
            user_id = data.get('user_id')
            if user_id is None:
                return jsonify(message='User ID is required'), 400

            receipts = Receipt_Model.query.filter_by(created_user_id=user_id).all()
            if receipts:
                receipt_list = []
                for receipt in receipts:
                    expenses = Expenses_Model.query.filter_by(user_id=user_id, receipt_id=receipt.receipt_id).all()
                    expense_data = [{
                        'expense_id': expense.expenses_id,
                        'share_amount': expense.share_amount
                    } for expense in expenses]

                    category = Category_Model.query.filter_by(user_id=user_id, category_id=receipt.cat_id).first()
                    category_name = category.category_name if category else None

                    recurring = Recurring_Frequency_Model.query.filter_by(recurring_id=receipt.recur_id).first()
                    recurring_name = recurring.recur_name if recurring else None

                    receipt_data = {
                        'receipt_id': receipt.receipt_id,
                        'title': receipt.title,
                        'description': receipt.description,
                        'created_datetime': receipt.created_datetime,
                        'group_id': receipt.group_id,
                        'recur_id': receipt.recur_id,
                        'cat_id': receipt.cat_id,
                        'icon_id': receipt.icon_id,
                        'updated_recur_datetime': receipt.updated_recur_datetime,
                        'category_name': category_name,
                        'recurring_name': recurring_name,
                        'expenses': expense_data  
                    }
                    receipt_list.append(receipt_data)
                return jsonify(receipts=receipt_list)
            else:
                return jsonify(message=f'No receipts found for user with ID {user_id}'), 404
                    
        except Exception as e:
            return jsonify(message=f'Error reading receipts: {str(e)}'), 500


    def update_expense(self, data):
        try:
            if 'id' not in data:
                return jsonify(message='Expense ID not specified in the request'), 400
            expense_id = data['id']
            expense = Expenses_Model.query.get(expense_id)
            if not expense:
                return jsonify(message=f'Expense with ID {expense_id} not found'), 404
            expense.name = data['name']
            expense.expenses = data['expenses']
            db.session.commit()
            return jsonify(message='Expense updated successfully!')
        except Exception as e:
            return jsonify(message=f'Error update expense: {str(e)}'), 500


    def delete_expense(self,data):
        try:
            receipt_id = data.get('receipt_id')

            if not receipt_id:
                return jsonify({'error': 'Receipt ID is required', 'status_code': 400}), 400

            receipt = Receipt_Model.query.get(receipt_id) #From receipt model
            if not receipt:
                return jsonify({'error': 'Receipt not found', 'status_code': 404}), 404

            expenses = Expenses_Model.query.filter_by(receipt_id=receipt_id).all() #From expense model
            if not expenses:
                return jsonify({'error': 'Expenses not found for this receipt', 'status_code': 404}), 404

            for expense in expenses:    #Delete expenses with receipt id
                db.session.delete(expense)

            # currency_conversions = Currency_Conversion_Model.query.filter_by(expense_id=expense_id).all()

            # for conversion in currency_conversions:
            #     db.session.delete(conversion)
            
            db.session.delete(receipt)  #Delete the receipts
            db.session.commit() 
            
            return jsonify({'message': 'Receipt & expenses deleted successfully.', 'status_code': 200}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error deleting receipt and expenses: {str(e)}', 'status_code': 500}), 500

    def split_expense(self, data):
        try:
            if 'groupId' not in data:
                return jsonify(message='Group ID not specified in the request'), 400
            else:
                group = Groups_Model.query.filter_by(group_id=data['groupId']).all()
                if not group:
                    return jsonify(message='Group Id is not valid.'), 400
                else:
                    grouping_response = self.grouping_utility.read_grouping_by_group_id({"groupId": data['groupId']})
                    grouping_response_content = grouping_response.get_data(as_text=True)
                    grouping_data = json.loads(grouping_response_content).get("grouping", [])
            
            
            if 'amount' in data:
                amount = data['amount']
                expenses_per_ppl = Decimal(amount) / Decimal(len(grouping_data))
                expenses_per_ppl = expenses_per_ppl.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
            else:
                return jsonify(message='Amount are not specified in the request',status_code='400'), 400

            return jsonify(expenses_per_ppl=expenses_per_ppl, status_code='200')

        except Exception as e:
            return jsonify(message=f'Error split expense: {str(e)}', status_code='500'), 500
        
   
        
    def create_expense(self, data):
        print(data)
        try:
            if "user_id" not in data:
                return jsonify(message='Invalid request. Please provide user id.', status_code=400), 400
            else:
                user = User_Model.query.filter_by(user_id=data['user_id']).all()
                if not user:
                    return jsonify(message='Invalid request. Please provide valid user id.', status_code=400), 400
            if "title" not in data:
                return jsonify(message='Invalid request. Please provide title.', status_code=400), 400
            if "description" not in data:
                data['description'] = None
            if "cat_id" not in data:
                return jsonify(message='Invalid request. Please provide category id.', status_code=400), 400
            else:
                category = Category_Model.query.filter_by(user_id=data['user_id'],category_id=data['cat_id']).all()
                if not category:
                    return jsonify(message='Invalid request. Please provide valid category id.', status_code=400), 400
            if "share_amount" not in data:
                return jsonify(message='Invalid request. Please provide share amount.', status_code=400), 400
            if "from_currency" not in data:
                return jsonify(message='Invalid request. Please provide from Currency.', status_code=400), 400
            else:
                currency = Currencies_Model.query.filter_by(currency_id=data['from_currency']).all()
                if not currency:
                    return jsonify(message='Invalid request. Please provide valid currency id.', status_code=400), 400
            if "icon_id" not in data:
                return jsonify(message='Invalid request. Please provide icon id.', status_code=400), 400
            else:
                icon = Icon_Model.query.filter_by(icon_id=data['icon_id']).all()
                if not icon:
                    return jsonify(message='Invalid request. Please provide valid icon id.', status_code=400), 400
            if "recur_id" in data:
                if data['recur_id'] is not None and data['recur_id'] !="":
                    recurring_frequency = Recurring_Frequency_Model.query.filter_by(recurring_id=data['recur_id']).all()
                    if not recurring_frequency:
                        return jsonify(message='Invalid request. Please provide valid recurring frequency id.', status_code=400), 400
            if "group_id" in data:
                if data['group_id'] is not None and data['group_id'] !="":
                    groups = Groups_Model.query.filter_by(group_id=data['group_id']).all()
                    if not groups:
                        return jsonify(message='Invalid request. Please provide valid group id.', status_code=400), 400
                    
            data['group_id'] = None if "group_id" not in data or data['group_id'] == "" else data['group_id']
            data['recur_id'] = None if "recur_id" not in data or data['recur_id'] == "" else data['recur_id']

            new_receipt = Receipt_Model(
                created_user_id=data['user_id'],
                title=data['title'],
                description=data['description'],
                created_datetime=datetime.utcnow(),
                group_id=data['group_id'],
                recur_id=data['recur_id'],
                cat_id=data['cat_id'],
                icon_id=data['icon_id'],
                updated_recur_datetime=datetime.utcnow(),
            )
            db.session.begin_nested()
            db.session.add(new_receipt)
            db.session.commit()

            currency_response_default_currency = self.currency_utility.read_all_currencies()

            if isinstance(currency_response_default_currency, tuple):
                currency_response_default_currency, status_code = currency_response_default_currency
            else:
                status_code = currency_response_default_currency.status_code
            if status_code != 200:
                currency_response_default_currency_content = currency_response_default_currency.get_data(as_text=True)
                db.session.rollback()
                #print("convert_currency_response_content (status code 500):", currency_response_default_currency_content)
                return jsonify(message=currency_response_default_currency_content), status_code

            currency_response_content = currency_response_default_currency.get_data(as_text=True)
            currency_data = json.loads(currency_response_content).get("currency")
            if currency_data:
                codes = [currency.get("code") for currency in currency_data]
                currency_ids = [currency.get("currency_id") for currency in currency_data]
                index_of_currency = currency_ids.index(int(data['from_currency']))
                from_currency = codes.pop(index_of_currency)
                from_currency_id = currency_ids.pop(index_of_currency)
                #print(codes)
                #print(currency_ids)
                countj = 0

                exchange_rates_n_coverted_amount = []

                for j in codes:
                    convert_currency_response = self.currency_utility.currency_converter_expense(
                        {"amount": data['share_amount'], "from_currency": from_currency, "to_currency": j})

                    if isinstance(convert_currency_response, tuple):
                        convert_currency_response, status_code = convert_currency_response
                    else:
                        status_code = convert_currency_response.status_code

                    if status_code != 200:
                        convert_currency_response_content = convert_currency_response.get_data(as_text=True)
                        db.session.rollback()
                        #print("convert_currency_response_content (status code 500/400):", convert_currency_response_content)
                        return jsonify(message=convert_currency_response_content), status_code

                    convert_currency_response_content = convert_currency_response.get_data(as_text=True)
                    #print("convert_currency_response_content:", convert_currency_response_content)

                    exchange_rates_n_coverted_amount.append(
                        {"exchange_rate": json.loads(convert_currency_response_content).get("exchange_rate"),
                         "converted_amount": json.loads(convert_currency_response_content).get("converted_amount")})
            else:
                db.session.rollback()
                return jsonify(message='No currencies inside database', status_code="400"), 400

            if data['group_id'] == None:
                new_expense = Expenses_Model(
                        user_id=data['user_id'],
                        share_amount=data['share_amount'],
                        receipt_id=new_receipt.receipt_id
                    )
                db.session.add(new_expense)
                db.session.commit()

                created_expense_id = new_expense.expenses_id

                convert_currency_reponse = self.currency_utility.create_currency_converter({
                    "original_currency": data['from_currency'],
                    "convert_currency": data['from_currency'],
                    "exchange_rate": 1,
                    "converted_amount": data['share_amount'],
                    "expense_id": created_expense_id,
                    "commit": "false"
                })

                countj = 0
                for j in codes:
                    # print("countj:", countj)
                    #print("j:", j)
                    #print("from_currency:", from_currency)
                    #print("currency_ids:", currency_ids)

                    convert_currency_reponse = self.currency_utility.create_currency_converter({
                        "original_currency": from_currency_id,
                        "convert_currency": currency_ids[countj],
                        "exchange_rate": exchange_rates_n_coverted_amount[countj].get("exchange_rate"),
                        "converted_amount": exchange_rates_n_coverted_amount[countj].get("converted_amount"),
                        "expense_id": created_expense_id,
                        "commit": "false"
                    })

                    if isinstance(convert_currency_reponse, tuple):
                        convert_currency_reponse, status_code = convert_currency_reponse
                    else:
                        status_code = convert_currency_reponse.status_code
                    if status_code != 200:
                        convert_currency_reponse_content = convert_currency_reponse.get_data(as_text=True)
                        db.session.rollback()
                        #print("convert_currency_response_content (status code 400/500):", convert_currency_reponse_content)
                        return jsonify(message=convert_currency_reponse_content), status_code

                    countj += 1
            else:
                grouping_response = self.grouping_utility.read_grouping_by_group_id({"groupId": data['group_id']})
                grouping_response_content = grouping_response.get_data(as_text=True)
                grouping_data = json.loads(grouping_response_content).get("grouping", [])
                print(grouping_data)
                grouping_ids = [group['user_id'] for group in grouping_data]

                for grouping_id in grouping_ids:
                    new_expense = Expenses_Model(
                        user_id=grouping_id,
                        share_amount=data['share_amount'],
                        receipt_id=new_receipt.receipt_id
                    )
                    db.session.add(new_expense)

                    db.session.commit()

                    created_expense_id = new_expense.expenses_id

                    convert_currency_reponse = self.currency_utility.create_currency_converter({
                        "original_currency": data['from_currency'],
                        "convert_currency": data['from_currency'],
                        "exchange_rate": 1,
                        "converted_amount": data['share_amount'],
                        "expense_id": created_expense_id,
                        "commit": "false"
                    })

                    countj = 0
                    for j in codes:
                        # print("countj:", countj)
                        #print("j:", j)
                        #print("from_currency:", from_currency)
                        #print("currency_ids:", currency_ids)

                        convert_currency_reponse = self.currency_utility.create_currency_converter({
                            "original_currency": from_currency_id,
                            "convert_currency": currency_ids[countj],
                            "exchange_rate": exchange_rates_n_coverted_amount[countj].get("exchange_rate"),
                            "converted_amount": exchange_rates_n_coverted_amount[countj].get("converted_amount"),
                            "expense_id": created_expense_id,
                            "commit": "false"
                        })

                        if isinstance(convert_currency_reponse, tuple):
                            convert_currency_reponse, status_code = convert_currency_reponse
                        else:
                            status_code = convert_currency_reponse.status_code
                        if status_code != 200:
                            convert_currency_reponse_content = convert_currency_reponse.get_data(as_text=True)
                            db.session.rollback()
                            #print("convert_currency_response_content (status code 400/500):", convert_currency_reponse_content)
                            return jsonify(message=convert_currency_reponse_content), status_code

                        countj += 1

            db.session.commit()

            return jsonify(message='Transaction created successfully!', status_code="200"), 200
        except Exception as e:
            db.session.rollback()
            return jsonify(message=f'Error creating expense: {str(e)}', status_code="500"), 500



