from flask import json
from config.database_config import db
import pytest
from model.user_model import User_Model
from model.forgot_password_model import Reset_Password_Model

@pytest.fixture(scope="function")
def setup():
    # Insert data for icons
    user_data = [
        ('Jun Jie', 'junjie.wee@ncs.com.sg', 'gAAAAABl_bQCWhpP8BZXFfY1HuNDuin_nvSFaSEwEIol-1Hv-MbYNfP9wX-m31l34QrbmHIvv4argsqho2WePmIgTvX0TDJgPA=='),
        ('Gerald', 'gerald.hoo@ncs.com.sg', 'gAAAAABl7uZHcn6ltKCWubI_t3Wu5J96Awvz3Jr-dR0dZ3YHrVV7MLlufoiATkek_eiA35SMyBeG0T76isaAgngQ4HagUN_lrg=='),
        ('Wei Zee', 'weizee@ncs.com.sg', 'gAAAAABl7uZHcn6ltKCWubI_t3Wu5J96Awvz3Jr-dR0dZ3YHrVV7MLlufoiATkek_eiA35SMyBeG0T76isaAgngQ4HagUN_lrg==')
    ]
    for user_name, email, password in user_data:
        user_model = User_Model(
            user_name=user_name,
            email=email,
            password=password
        )
        db.session.add(user_model)
    reset_password_data = [
        ('2', 'V7AH--vvtf5cxzqP86qFEL-CwTVAona4gG8DtES-MSA')
    ]
    for user_id, reset_token in reset_password_data:
        reset_password_model = Reset_Password_Model(
            user_id=user_id,
            reset_token=reset_token
        )
        db.session.add(reset_password_model)
    db.session.commit()
    yield

def test_all_user_by_email_successed(client,init_db,setup):
    data = {"email": "junjie.wee@ncs.com.sg"}

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/user/readUser', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)


    assert status_code == 200
    assert data['user'] == {
        "bio": None,
        "email": "junjie.wee@ncs.com.sg",
        "first_name": None,
        "last_name": None,
        "password": "gAAAAABl_bQCWhpP8BZXFfY1HuNDuin_nvSFaSEwEIol-1Hv-MbYNfP9wX-m31l34QrbmHIvv4argsqho2WePmIgTvX0TDJgPA==",
        "user_id": 1,
        "user_name": "Jun Jie"
    }

def test_all_user_by_id_successed(client):
    data = {"user_id": "1"}

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/user/readUser', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)


    assert status_code == 200
    assert data['user'] == {
        "bio": None,
        "email": "junjie.wee@ncs.com.sg",
        "first_name": None,
        "last_name": None,
        "password": "gAAAAABl_bQCWhpP8BZXFfY1HuNDuin_nvSFaSEwEIol-1Hv-MbYNfP9wX-m31l34QrbmHIvv4argsqho2WePmIgTvX0TDJgPA==",
        "user_id": 1,
        "user_name": "Jun Jie"
    }

def test_read_user_without_user_id_email_failed(client):
    data = {}

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/user/readUser', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == "Invalid request. Please provide user id or email."


def test_read_user_invalid_user_id_failed(client):
    data = {
        "user_id": "10000"
    }

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/user/readUser', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 404
    assert data["message"].startswith("User with ID")

def test_login_successed(client):
    data = {
        "email": "gerald.hoo@ncs.com.sg",
        "password": "default1111"
    }

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/user/login', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 200
    assert data["user_id"] == 2

def test_login_failed(client):
    data = {
        "email": "gerald.hoo@ncs.com.sg",
        "password": "haha"
    }

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/user/login', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400

def test_login_without_email_failed(client):
    data = {
        "password": "haha"
    }

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/user/login', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data["message"]=="Invalid request. Please provide email."

def test_login_without_password_failed(client):
    data = {
        "email": "gerald.hoo@ncs.com.sg"
    }

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/user/login', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data["message"]=="Invalid request. Please provide password."

def test_login_without_password_failed(client):
    data = {
        "email": "hehe",
        "password": "hoho"
    }

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/user/login', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data["message"]=="Cannot found user"

def test_forgot_password_successed(client):
    data = {
        "email": "junjie.wee@ncs.com.sg"
    }

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/user/forgotPassword', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 200
    assert data["message"]=="Password reset email sent successfully."

def test_forgot_password_without_email_failed(client):
    data = {
    }

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/user/forgotPassword', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data["message"]=="Invalid request. Please provide email."

def test_forgot_password_invalid_email_failed(client):
    data = {
        "email": "hehe"
    }

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/user/forgotPassword', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 404
    assert data["message"]=="Email not found."

def test_change_password_successed(client):
    data = {
        "email": "gerald.hoo@ncs.com.sg",
        "new_password": "default1111",
        "token": "V7AH--vvtf5cxzqP86qFEL-CwTVAona4gG8DtES-MSA"
    }

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/user/changePassword', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 200
    assert data["message"]=="Password updated successfully!"

def test_change_password_invalid_token_failed(client):
    data = {
        "email": "gerald.hoo@ncs.com.sg",
        "new_password": "default1111",
        "token": "abc"
    }

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/user/changePassword', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 404
    assert data["message"]=="User with token None not found"

def test_change_password_invalid_token_failed(client):
    data = {
        "email": "junjie.wee@ncs.com.sg",
        "new_password": "default1111",
        "token": "V7AH--vvtf5cxzqP86qFEL-CwTVAona4gG8DtES-MSA"
    }

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/user/changePassword', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data["message"]=="Wrong token provided."

def test_change_password_without_email_failed(client):
    data = {
        "new_password": "default1111",
        "token": "V7AH--vvtf5cxzqP86qFEL-CwTVAona4gG8DtES-MSA"
    }

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/user/changePassword', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data["message"]=="Invalid request. Please provide email."

def test_change_password_without_new_password_failed(client):
    data = {
        "email": "gerald.hoo@ncs.com.sg",
        "token": "V7AH--vvtf5cxzqP86qFEL-CwTVAona4gG8DtES-MSA"
    }

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/user/changePassword', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data["message"]=="Invalid request. Please provide new password."

def test_change_password_without_token_failed(client):
    data = {
        "email": "gerald.hoo@ncs.com.sg",
        "new_password": "default1111"
    }

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/user/changePassword', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data["message"]=="Invalid request. Please provide token."

def test_create_user_success(client):
    data = {
        "user_name": "john_wick",
        "email": "john.wick@NCS.com",
        "password": "password123",
        "first_name": "John",
        "last_name": "Wick"
    }
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}

    response = client.post('/user/createUser', data=json_data, headers=headers)

    assert response.status_code == 201
    assert "user_id" in json.loads(response.data)["user"]

def test_create_user_duplicate_username(client):
    data = {
        "user_name": "Gerald",
        "email": "john.wick@NCS.com",
        "password": "password123",
        "first_name": "John",
        "last_name": "Wick"
    }
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}

    response = client.post('/user/createUser', data=json_data, headers=headers)

    assert response.json['user_status_code'] == 501
    assert "Username already exists!" in response.json['message']

def test_create_user_duplicate_email(client):
    data = {
        "user_name": "john_wick",
        "email": "junjie.wee@ncs.com.sg",
        "password": "password123",
        "first_name": "John",
        "last_name": "Wick"
    }
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}

    response = client.post('/user/createUser', data=json_data, headers=headers)

    assert response.json['user_status_code'] == 501
    assert "Email already exists!" in response.json['message']










