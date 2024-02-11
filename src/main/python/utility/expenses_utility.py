from flask import jsonify, request
from config.database_config import db
from model.expenses_model import Expenses_Model
from utility.grouping_utility import Grouping_Utility
import json
import base64
from forex_python.converter import CurrencyRates

class Expenses_Utility:
    def __init__(self):
        self.grouping_utility = Grouping_Utility()


    def create_expense(self, data):
        try:
            new_expense = Expenses_Model(name=data['name'], expenses=data['expenses'])
            db.session.add(new_expense)
            db.session.commit()
            return jsonify(message='Expense created successfully!')
        except Exception as e:
            return jsonify(message=f'Error creating expense: {str(e)}'), 500

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
                expense_list = [{'id': expense.id, 'name': expense.name, 'expenses': expense.expenses} for expense in expenses]
                return jsonify(expenses=expense_list)
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
            if 'expenseId' not in data:
                return jsonify(message='Expense ID not specified in the request'), 400
            if 'groupId' not in data:
                return jsonify(message='Group ID not specified in the request'), 400
                
            expenses_response = self.read_expenses({"id": data['expenseId']})
            grouping_response = self.grouping_utility.read_grouping_by_group_id({"groupId": data['groupId']})
            grouping_response_content = grouping_response.get_data(as_text=True)
            grouping_data = json.loads(grouping_response_content).get("grouping", [])
            expenses_response_content = expenses_response.get_data(as_text=True)
            expenses_data = json.loads(expenses_response_content).get("expenses")

            expenses_per_ppl =  round(int(expenses_data) / len(grouping_data), 2)
            

            return jsonify(expenses_per_ppl=expenses_per_ppl)

        except Exception as e:
            return jsonify(message=f'Error split expense: {str(e)}'), 500
        
    def currency_converter_expense(self, data):
        try:
            if 'amount' not in data:
                    return jsonify(message='Amount not specified in the request'), 400
            if 'from_currency' not in data:
                return jsonify(message='From Currency not specified in the request'), 400
            if 'to_currency' not in data:
                return jsonify(message='To Currency not specified in the request'), 400
            c = CurrencyRates()
            amount = data['amount']
            from_currency = data['from_currency']
            to_currency = data['to_currency']
            exchange_rate = c.get_rate(from_currency, to_currency)
            converted_amount = round(float(amount) * float(exchange_rate), 2)
            return jsonify(converted_amount=converted_amount)
        except Exception as e:
            return jsonify(message=f'Error convert currency: {str(e)}'), 500

