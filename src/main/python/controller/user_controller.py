from flask import jsonify, request
from config.database_config import db
from utility.user_utility import User_Utility

class User_Controller:
    def __init__(self, app):
        self.app = app
        self.user_utility = User_Utility()
        
        # Gerald - WIP: DO NOT TOUCH
        @app.route('/users', methods=["POST"])
        def create_user():
            # Get user data from request
            user_name = request.form['user_name']
            email = request.form['email']
            password = request.form['password']
            account_status = request.form['account_status']

            # Create a user instance
            user_db = User_Utility()
            user = user_db.create_user(user_name, email, password, account_status)

            if user:
                return jsonify(message='User created successfully', user=user), 201
            else:
                return jsonify(message='Failed to create user', user=None), 500


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
        
        @app.route('/user/changePassword', methods=['POST'])
        def change_password():
            data = request.get_json()
            return self.user_utility.change_password(data)