from flask import jsonify, request
from model.recurring_frequency_model import Recurring_Frequency_Model
from model.receipt_model import Receipt_Model;
from datetime import datetime, timedelta
from utility.expenses_utility import Expenses_Utility
from config.database_config import db

class Recurring_Frequency_Utility:

    def __init__(self):
        self.expenses_utility = Expenses_Utility()
        
    def read_all_recurring_frequency(self, data=None):
        try:
            if not bool(data):
                recurring_frequencies = Recurring_Frequency_Model.query.all()
                if recurring_frequencies:
                    recurring_frequency_list = [{'recurring_id': recurring_frequency.recurring_id, 'recur_name': recurring_frequency.recur_name} for recurring_frequency in recurring_frequencies]
                    return jsonify(recurring_frequency=recurring_frequency_list, status_code='200')
                else:
                    return jsonify(message='Recurring frequencies are not found', status_code='404'), 404
            else:
                recurring_id = data.get('recurring_id')
                recurring_frequency = Recurring_Frequency_Model.query.get(recurring_id)
                if recurring_frequency:
                    return jsonify(recurring_id=recurring_frequency.recurring_id, recur_name=recurring_frequency.recur_name, status_code='200'), 200
                else:
                    return jsonify(message=f'Recurring frequency with ID {recurring_id} not found', status_code='404'), 404
        except Exception as e:
            return jsonify(message=f'Error reading recurring frequencies: {str(e)}', status_code='500'), 500
        

    def recurring_scheduler(self):
        try:
            receipts = Receipt_Model.query.filter(Receipt_Model.recur_id != "null").all()
            current_datetime = datetime.utcnow()
            if receipts:
                for receipt in receipts:
                    updated_recur_datetime = receipt.updated_recur_datetime
                    difference = current_datetime - updated_recur_datetime
                    months_difference = (current_datetime.year - updated_recur_datetime.year) * 12 + (current_datetime.month - updated_recur_datetime.month)
                    if receipt.recur_id=="1" and difference.days==1:
                        create_expense_response = self.expenses_utility.create_expense({"user_id": receipt.created_user_id,
                                                                "group_id": receipt.group_id,
                                                                "title": receipt.title,
                                                                "description": receipt.description,
                                                                "cat_id": receipt.cat_id,
                                                                "share_amount": receipt.created_user_id,
                                                                "from_currency": 1,
                                                                "icon_id": receipt.icon_id,
                                                                "recur_id": ""
                                                                })
                        if isinstance(create_expense_response, tuple):
                            create_expense_response, status_code = create_expense_response
                            create_expense_response_content = create_expense_response.get_data(as_text=True)
                            print(create_expense_response_content)
                        if status_code == 200:
                            update_receipt = Receipt_Model.query.get(receipt.receipt_id)
                            update_receipt.updated_recur_datetime = current_datetime
                            db.session.commit()
                    elif receipt.recur_id=="3" and difference.days==7:
                        create_expense_response = self.expenses_utility.create_expense({"user_id": receipt.created_user_id,
                                                                "group_id": receipt.group_id,
                                                                "title": receipt.title,
                                                                "description": receipt.description,
                                                                "cat_id": receipt.cat_id,
                                                                "share_amount": receipt.created_user_id,
                                                                "from_currency": 1,
                                                                "icon_id": receipt.icon_id,
                                                                "recur_id": ""
                                                                })
                        if isinstance(create_expense_response, tuple):
                            create_expense_response, status_code = create_expense_response
                            create_expense_response_content = create_expense_response.get_data(as_text=True)
                            print(create_expense_response_content)
                        if status_code == 200:
                            update_receipt = Receipt_Model.query.get(receipt.receipt_id)
                            update_receipt.updated_recur_datetime = current_datetime
                            db.session.commit()
                    elif receipt.recur_id=="3" and months_difference==1:
                        create_expense_response = self.expenses_utility.create_expense({"user_id": receipt.created_user_id,
                                                                "group_id": receipt.group_id,
                                                                "title": receipt.title,
                                                                "description": receipt.description,
                                                                "cat_id": receipt.cat_id,
                                                                "share_amount": receipt.created_user_id,
                                                                "from_currency": 1,
                                                                "icon_id": receipt.icon_id,
                                                                "recur_id": ""
                                                                })
                        if isinstance(create_expense_response, tuple):
                            create_expense_response, status_code = create_expense_response
                            create_expense_response_content = create_expense_response.get_data(as_text=True)
                            print(create_expense_response_content)
                        if status_code == 200:
                            update_receipt = Receipt_Model.query.get(receipt.receipt_id)
                            update_receipt.updated_recur_datetime = current_datetime
                            db.session.commit()
                    elif receipt.recur_id=="4" and months_difference==12:
                        create_expense_response = self.expenses_utility.create_expense({"user_id": receipt.created_user_id,
                                                                "group_id": receipt.group_id,
                                                                "title": receipt.title,
                                                                "description": receipt.description,
                                                                "cat_id": receipt.cat_id,
                                                                "share_amount": receipt.created_user_id,
                                                                "from_currency": 1,
                                                                "icon_id": receipt.icon_id,
                                                                "recur_id": ""
                                                                })
                        if isinstance(create_expense_response, tuple):
                            create_expense_response, status_code = create_expense_response
                            create_expense_response_content = create_expense_response.get_data(as_text=True)
                            print(create_expense_response_content)
                        if status_code == 200:
                            update_receipt = Receipt_Model.query.get(receipt.receipt_id)
                            update_receipt.updated_recur_datetime = current_datetime
                            db.session.commit()
            print("Sucessfully")
            # return jsonify(status_code='200'), 200
        except Exception as e:
            # return jsonify(message=f'Error reading recurring frequencies: {str(e)}', status_code='500'), 500
            print(f'Error reading recurring frequencies: {str(e)}')


