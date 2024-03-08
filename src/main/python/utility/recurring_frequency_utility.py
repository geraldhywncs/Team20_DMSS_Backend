from flask import jsonify, request
from model.recurring_frequency_model import Recurring_Frequency_Model

class Recurring_Frequency_Utility:

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
                    return jsonify(recurring_id=recurring_frequency.recurring_id, recur_name=recurring_frequency.recur_name, status_code='200')
                else:
                    return jsonify(message=f'Recurring frequency with ID {recurring_id} not found', status_code='404'), 404
        except Exception as e:
            return jsonify(message=f'Error reading recurring frequencies: {str(e)}', status_code='500'), 500

