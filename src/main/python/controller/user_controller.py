from flask import jsonify, request
from config.database_config import db
from utility.user_utility import User_Utility

class User_Controller:
    def __init__(self, app):
        self.app = app
        self.user_utility = User_Utility()
        with app.app_context():
            db.create_all()

        @app.route('/user/id', methods=["GET"])
        def get_user(user_id):
            return self.user_utility.get_user(user_id)


        @app.route('/user/readUser', methods=['POST'])
        def read_user():
            data = request.get_json()
            return self.user_utility.read_user(data)
        
        @app.route('/user/login', methods=['POST'])
        def login():
            data = request.get_json()
            return self.user_utility.login(data)
        
        @app.route('/user/forgotPassword', methods=['POST'])
        def forgot_password():
            data = request.get_json()
            return self.user_utility.forgot_password(data)