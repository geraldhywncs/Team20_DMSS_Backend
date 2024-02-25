from flask import jsonify, request
from config.database_config import db
from model.expenses_model import Expenses_Model
from utility.grouping_utility import Grouping_Utility
from utility.currency_utility import Currency_Utility
import json
import base64
from forex_python.converter import CurrencyRates
from decimal import Decimal, ROUND_HALF_UP
import requests
import time

class Expenses_Utility:
    def __init__(self):
        self.grouping_utility = Grouping_Utility()
        self.currency_utility = Currency_Utility()

    def read_expenses(self, data):
        try:
            expense_id = data.get('id')
            if expense_id is not None:
                expense = Expenses_Model.query.get(expense_id)
                if expense:
                    return jsonify(id=expense.id, name=expense.name, expenses=expense.expenses)
                else:
                    return jsonify(message=f'Expense with ID {expense_id} not found'), 404
            else:
                expenses = Expenses_Model.query.all()
                if expenses:
                    expense_list = [{'id': expense.id, 'name': expense.name, 'expenses': expense.expenses} for expense in expenses]
                    return jsonify(expenses=expense_list)
                else:
                    return jsonify(message=f'Expenses are not found'), 404
                
        except Exception as e:
            return jsonify(message=f'Error reading expenses: {str(e)}'), 500


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
            if 'id' not in data:
                return jsonify(message='Expense ID not specified in the request'), 400
            expense_id = data['id']
            expense = Expenses_Model.query.get(expense_id)
            if not expense:
                return jsonify(message=f'Expense with ID {expense_id} not found'), 404
            db.session.delete(expense)
            db.session.commit()
            return jsonify(message='Expense deleted successfully!')
        except Exception as e:
            return jsonify(message=f'Error delete expense: {str(e)}'), 500

    
    def split_expense(self, data):
        try:
            if 'groupId' not in data:
                return jsonify(message='Group ID not specified in the request'), 400
            else:
                grouping_response = self.grouping_utility.read_grouping_by_group_id({"groupId": data['groupId']})
                grouping_response_content = grouping_response.get_data(as_text=True)
                grouping_data = json.loads(grouping_response_content).get("grouping", [])
                

            if 'expenseId' in data and 'amount' not in data:
                expenses_response = self.read_expenses({"expenses_id": data['expenseId']})
                expenses_response_content = expenses_response.get_data(as_text=True)
                expenses_data = json.loads(expenses_response_content).get("expenses")
                expenses_per_ppl = Decimal(expenses_data) / Decimal(len(grouping_data))
                expenses_per_ppl = expenses_per_ppl.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
            elif 'expenseId' not in data and 'amount' in data:
                amount = data['amount']
                expenses_per_ppl = Decimal(amount) / Decimal(len(grouping_data))
                expenses_per_ppl = expenses_per_ppl.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
            elif 'expenseId' in data and 'amount' in data:
                return jsonify(message='Which do you have to count at? Expense ID or Amount'), 400
            else:
                return jsonify(message='Expense ID and Amount are not specified in the request'), 400

            return jsonify(expenses_per_ppl=expenses_per_ppl)

        except Exception as e:
            return jsonify(message=f'Error split expense: {str(e)}'), 500
        
   
        
    def create_expense(self, data):
        try:
            if "userId" not in data:
                return jsonify(message='Invalid request. Please provide user id.'), 400
            if "groupId" not in data:
                data['groupId'] = None
            if "title" not in data:
                return jsonify(message='Invalid request. Please provide title.'), 400
            if "description" not in data:
                data['description'] = None
            if "catId" not in data:
                return jsonify(message='Invalid request. Please provide category id.'), 400
            if "recurExpense" not in data:
                data['recurExpense'] = None
            if "shareAmount" not in data:
                data['shareAmount'] = None
            if "amount" not in data:
                return jsonify(message='Invalid request. Please provide amount.'), 400
            
            new_expense = Expenses_Model(
                                user_id = data['userId'], 
                                group_id = data['groupId'],
                                title = data['title'],
                                description = data['description'],
                                cat_id = data['catId'],
                                recur_expense = data['recurExpense'],
                                share_amount = data['shareAmount']
                            )
            db.session.add(new_expense)
            db.session.commit()

            created_expense_id = new_expense.expenses_id
            
            currency_response_default_currency = self.currency_utility.read_all_currencies()
            print(currency_response_default_currency)
            currency_response_content = currency_response_default_currency.get_data(as_text=True)
            currency_data = json.loads(currency_response_content).get("currency")

            if currency_data:
                codes = [currency.get("code") for currency in currency_data]
                currency_ids = [currency.get("currency_id") for currency in currency_data]
                convert_list = []
                counti = 0
                countj = 0

                for i in codes:
                    for j in codes:
                        convert_currency_response = self.currency_utility.currency_converter_expense({"amount": data['amount'], "from_currency": i, "to_currency": j})
                        print("convert_currency_response:", convert_currency_response)

                        # Check if the response is a tuple
                        if isinstance(convert_currency_response, tuple):
                            # Extract the response from the tuple
                            convert_currency_response, status_code = convert_currency_response
                        else:
                            # If not a tuple, set the status_code to the response's status code
                            status_code = convert_currency_response.status_code

                        # Check the status code of the response
                        if status_code == 500:
                            print("Skipping due to status code 500")
                            # Print the content of convert_currency_response_content
                            convert_currency_response_content = convert_currency_response.get_data(as_text=True)
                            print("convert_currency_response_content (status code 500):", convert_currency_response_content)
                            continue

                        # Introduce a sleep time (e.g., 1 second) between requests
                        #time.sleep(1)

                        convert_currency_response_content = convert_currency_response.get_data(as_text=True)
                        print("convert_currency_response_content:", convert_currency_response_content)

                        # Print values to identify where the error occurs
                        print("counti:", counti, "countj:", countj)
                        print("i:", i, "j:", j)
                        print("currency_ids:", currency_ids)

                        # ... (rest of the code)
                        convert_currency_reponse = self.currency_utility.create_currency_converter({
                            "original_currency": currency_ids[counti],
                            "convert_currency": currency_ids[countj],
                            "exchange_rate": json.loads(convert_currency_response_content).get("exchange_rate"),
                            "converted_amount": json.loads(convert_currency_response_content).get("converted_amount"),
                            "expense_id": created_expense_id
                        })

                        countj += 1
                    countj = 0
                    counti += 1

            else:
                return jsonify(message='No currencies inside database'), 400

            
            return jsonify(message='Expense created successfully!')
        except Exception as e:
            return jsonify(message=f'Error creating expense: {str(e)}'), 500



