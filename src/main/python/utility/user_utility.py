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
    def create(self, user_name, email, password, first_name, last_name):
        try:
            user = User_Model(user_name=user_name, email=email, password=password, first_name=first_name, last_name=last_name, bio='')
            db.session.add(user)
            db.session.commit()
            return user.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return f'Error in User_Utility.create(): {str(e)}', 500

    def get(self, user_id):
        try:
            user = db.session.get(User_Model, user_id)
            if user is not None:
                return user.to_dict(), 200
            else:
                return 'User not found', 404
        except Exception as e:
            return f'Error in User_Utility.get(): {str(e)}', 500
        
    def list_by_user_ids(self, user_ids):
        try:
            print(user_ids)
            users = User_Model.query.filter(User_Model.user_id.in_(user_ids)).all()
            users_list = [user.to_dict() for user in users]
            return users_list, 200
        except Exception as e:
            return f'Error in User_Utility.list_by_user_ids(): {str(e)}', 500
            

        
    def read_user(self, data):
        try:
            if "email" not in data and "user_id" not in data:
                return jsonify(message='Invalid request. Please provide user id or email.', status_code=400), 400
            elif "email" in data and "user_id" not in data:
                email = data.get('email')
                user = User_Model.query.filter_by(email=email).first()
                if user:
                    return jsonify(user=user.to_dict(), status_code="200"), 200
                else:
                    return jsonify(message=f'User with email {email} not found', status_code='404'), 404
            elif "user_id" in data and "email" not in data:
                user_id = data.get('user_id')
                user = db.session.get(User_Model, user_id)
                if user:
                    return jsonify(user=user.to_dict(), status_code="200"), 200
                else:
                    return jsonify(message=f'User with ID {user_id} not found', status_code='404'), 404
        except Exception as e:
            return jsonify(message=f'Error reading user: {str(e)}', status_code="500"), 500
    
    def read_fernet_key(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(current_dir, '..', 'config.ini')
        config = ConfigParser()
        config.read(config_file_path)
        PASSWORD_FERNET_KEY = config.get('password', 'PASSWORD_FERNET_KEY')
        return PASSWORD_FERNET_KEY
    
    def read_reset_password_url(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(current_dir, '..', 'config.ini')
        config = ConfigParser()
        config.read(config_file_path)
        RESETPASSWORD = config.get('url', 'RESETPASSWORD')
        return RESETPASSWORD

    def decrypt_password(self, password):
        key = self.read_fernet_key()
        print(key)
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
                user_password = user_data.get("user").get("password")
                print(user_password)
                decrypted_password = self.decrypt_password(user_password)
                print(f"decrypted_password {decrypted_password}")
                print(f"data.get('email') {data.get('email')}")
                if decrypted_password == data.get('password'):
                    user_id = user_data.get("user").get("user_id")
                    return jsonify(user_id=user_id, status_code="200"), 200
                else:
                    return jsonify(status_code="400"), 400
            else:
                return jsonify(message="Cannot found user", status_code="400"), 400            
        except Exception as e:
            return jsonify(message=f'Error login: {str(e)}', status_code="500"), 500
    
    def forgot_password(self, data):
        try:
            if "email" not in data:
                return jsonify(message='Invalid request. Please provide email.', status_code=400), 400
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
                    user_id = user_data.get("user").get("user_id"),
                    reset_token = reset_token
                )
                db.session.begin_nested()
                db.session.add(new_reset_password)
                db.session.commit()
                RESETPASSWORD = self.read_reset_password_url()
                reset_link = f'{RESETPASSWORD}email={email}&token={reset_token}'
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

    def change_password(self, data):
        try:
            if "email" not in data:
                    return jsonify(message='Invalid request. Please provide email.', status_code=400), 400
            if "new_password" not in data:
                    return jsonify(message='Invalid request. Please provide new password.', status_code=400), 400
            if "token" not in data:
                    return jsonify(message='Invalid request. Please provide token.', status_code=400), 400
            email = data.get('email')
            new_password = data.get('new_password')
            reset_token = data.get('token')
            user = User_Model.query.filter_by(email=email).first()
            if not user:
                return jsonify(message=f'User with email {email} not found'), 404
            else:
                token = Reset_Password_Model.query.filter_by(reset_token=reset_token).first()
                if not token:
                    return jsonify(message=f'User with token {token} not found'), 404
                else:
                    print(token.user_id)
                    print(user.user_id)
                    if token.user_id == user.user_id:
                        user.password = self.encrypt_password(new_password.encode('utf-8'))
                        db.session.commit()
                        return jsonify(message='Password updated successfully!', status_code="200"), 200
                    else:
                        return jsonify(message='Wrong token provided.', status_code="400"), 400
        except Exception as e:
            return jsonify(message=f'Error update user: {str(e)}', status_code="500"), 500

