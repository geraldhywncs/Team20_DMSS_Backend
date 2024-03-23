from flask import jsonify, request
from model.icon_model import Icon_Model
from config.database_config import db

class Icon_Utility:

    def read_all_icon(self, data=None):
        try:
            if not bool(data):
                icons = Icon_Model.query.all()
                if icons:
                    icons_list = [{'icon_id': icon.icon_id, 'icon_name': icon.icon_name} for icon in icons]
                    return jsonify(icons=icons_list, status_code='200')
                else:
                    return jsonify(message='Icons are not found', status_code='404'), 404
            else:
                icon_id = data.get('icon_id')
                icon = db.session.get(Icon_Model, icon_id)
                if icon:
                    return jsonify(icon_id=icon.icon_id, icon_name=icon.icon_name, status_code='200')
                else:
                    return jsonify(message=f'Icon with ID {icon_id} not found', status_code='404'), 404
        except Exception as e:
            return jsonify(message=f'Error reading recurring frequencies: {str(e)}', status_code='500'), 500

