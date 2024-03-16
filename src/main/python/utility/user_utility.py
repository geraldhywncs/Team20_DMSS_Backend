from flask import jsonify
from config.database_config import db
from model.user_model import User_Model
from model.forgot_password_model import Reset_Password_Model
import json
from configparser import ConfigParser
import os
from cryptography.fernet import Fernet
import secrets

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass



class User_Utility:
    # def __init__(self):

    def read_user(self, data):
        try:
            if "email" not in data and "user_id" not in data:
                return jsonify(message='Invalid request. Please provide user id or email.', status_code=400), 400
            elif "email" in data and "user_id" not in data:
                print("email")
                email = data.get('email')
                user = User_Model.query.filter_by(email=email).first()
                print(user)
                if user:
                    return jsonify(user_id=user.user_id, user_name=user.user_name, email=user.email, password=user.password, account_status=user.account_status, status_code="200"), 200
            elif "user_id" in data and "email" not in data:
                print("user_id")
                user_id = data.get('user_id')
                user = User_Model.query.get(user_id)
                if user:
                    return jsonify(user_id=user.user_id, user_name=user.user_name, email=user.email, password=user.password, account_status=user.account_status, status_code="200"), 200
        except Exception as e:
            return jsonify(message=f'Error reading user: {str(e)}', status_code="500"), 500
    
    def read_fernet_key(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(current_dir, '..', 'config.ini')
        config = ConfigParser()
        config.read(config_file_path)
        PASSWORD_FERNET_KEY = config.get('password', 'PASSWORD_FERNET_KEY')
        return PASSWORD_FERNET_KEY

    def decrypt_password(self, password):
        key = self.read_fernet_key()
        cipher_suite = Fernet(key)
        return cipher_suite.decrypt(password).decode()
    
    def encrypt_password(self, password):
        key = self.read_fernet_key()
        cipher_suite = Fernet(key)
        return cipher_suite.encrypt(password)
    
    def generate_fernet_key():
        return Fernet.generate_key()

    def login(self, data):
        try:
            if "email" not in data:
                return jsonify(message='Invalid request. Please provide email.', status_code=400), 400
            if "password" not in data:
                return jsonify(message='Invalid request. Please provide password.', status_code=400), 400
            
            user_response = self.read_user({"email": data.get('email')})

            if isinstance(user_response, tuple):
                user_response, status_code = user_response
            else:
                status_code = user_response.status_code

            if status_code == 200:
                user_response_content = user_response.get_data(as_text=True)
                user_data = json.loads(user_response_content)
                user_password = user_data.get("password")
                decrypted_password = self.decrypt_password(user_password)
                print(f"decrypted_password {decrypted_password}")
                print(f"data.get('email') {data.get('email')}")
                if decrypted_password == data.get('password'):
                    user_id = user_data.get("user_id")
                    return jsonify(user_id=user_id, status_code="200"), 200
                else:
                    return jsonify(status_code="400"), 400
            else:
                return jsonify(message="Cannot found user", status_code="400"), 400            
        except Exception as e:
            return jsonify(message=f'Error login: {str(e)}', status_code="500"), 500
    
    def forgot_password(self, data):
        try:
            email = data.get('email')
            user_response = self.read_user({"email": email})
            if isinstance(user_response, tuple):
                user_response, status_code = user_response
            else:
                status_code = user_response.status_code

            if status_code == 200:
                reset_token = secrets.token_urlsafe(32)
                user_response_content = user_response.get_data(as_text=True)
                user_data = json.loads(user_response_content)
                new_reset_password = Reset_Password_Model(
                    user_id = user_data.get("user_id"),
                    reset_token = reset_token
                )
                db.session.begin_nested()
                db.session.add(new_reset_password)
                db.session.commit()

                reset_link = f"https://example.com/reset-password?token={reset_token}"
                print(f"Reset link: {reset_link}")
                self.send_reset_password_email(reset_link, email)
                return jsonify(message='Password reset email sent successfully.', status_code=200)

            return jsonify(message='Email not found.', status_code=404), 404

        except Exception as e:
            return jsonify(message=f'Error: {str(e)}', status_code=500), 500
        
    def send_reset_password_email(self, reset_link, email):
    
        smtp_server = 'localhost'
        smtp_port = 25
        smtp_username = email
        # smtp_password = ''
        
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = email
        msg['Subject'] = 'Reset Password'

        msg.attach(MIMEText(reset_link, 'plain'))

        try:
            # with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:   
                # Login to the email server
                # server.login(smtp_username, smtp_password)
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                # Send the email
                server.sendmail(smtp_username, 'junjie.wee@ncs.com.sg', msg.as_string())
            return jsonify(message='Email sent successfully', status_code=200), 200
    
        except Exception as e:
            return jsonify(message='Error sending email: {e}', status_code=500), 500


