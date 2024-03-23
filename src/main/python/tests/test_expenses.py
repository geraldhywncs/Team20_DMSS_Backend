import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from main import app
from flask import json
import pytest


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_create_expenses_successed(client):
    expenses_data = {
        "user_id": "1",
        "group_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "share_amount": "500",
        "from_currency": "1",
        "icon_id": "1",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 200
    assert data['message'] == 'Transaction created successfully!'

def test_create_expenses_without_group_id_recur_id_successed(client):
    expenses_data = {
        "user_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "share_amount": "500",
        "from_currency": "1",
        "icon_id": "1",
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 200
    assert data['message'] == 'Transaction created successfully!'
    
def test_create_expenses_no_user_id_pass_failed(client):
    expenses_data = {
        "group_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "share_amount": "500",
        "from_currency": "1",
        "icon_id": "1",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide user id.'

def test_create_expenses_no_cat_id_pass_failed(client):
    expenses_data = {
        "user_id": "1",
        "group_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "share_amount": "500",
        "from_currency": "1",
        "icon_id": "1",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide category id.'

def test_create_expenses_no_title_pass_failed(client):
    expenses_data = {
        "user_id": "1",
        "group_id": "1",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "share_amount": "500",
        "from_currency": "1",
        "icon_id": "1",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide title.'

def test_create_expenses_no_share_amount_pass_failed(client):
    expenses_data = {
        "user_id": "1",
        "group_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "from_currency": "1",
        "icon_id": "1",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide share amount.'

def test_create_expenses_no_from_currency_pass_failed(client):
    expenses_data = {
        "user_id": "1",
        "group_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "share_amount": "500",
        "icon_id": "1",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide from Currency.'

def test_create_expenses_no_icon_id_pass_failed(client):
    expenses_data = {
        "user_id": "1",
        "group_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "share_amount": "500",
        "from_currency": "1",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide icon id.'

def test_create_expenses_invalid_user_id_failed(client):
    expenses_data = {
        "user_id": "100000",
        "group_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "share_amount": "500",
        "from_currency": "1",
        "icon_id": "1",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide valid user id.'

def test_create_expenses_invalid_group_id_failed(client):
    expenses_data = {
        "user_id": "1",
        "group_id": "100000",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "share_amount": "500",
        "from_currency": "1",
        "icon_id": "1",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide valid group id.'

def test_create_expenses_invalid_cat_id_failed(client):
    expenses_data = {
        "user_id": "1",
        "group_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "100000",
        "share_amount": "500",
        "from_currency": "1",
        "icon_id": "1",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide valid category id.'

def test_create_expenses_invalid_from_currency_failed(client):
    expenses_data = {
        "user_id": "1",
        "group_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "share_amount": "500",
        "from_currency": "100000",
        "icon_id": "1",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide valid currency id.'

def test_create_expenses_invalid_icon_id_failed(client):
    expenses_data = {
        "user_id": "1",
        "group_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "share_amount": "500",
        "from_currency": "1",
        "icon_id": "100000",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide valid icon id.'

def test_create_expenses_invalid_recur_id_failed(client):
    expenses_data = {
        "user_id": "1",
        "group_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "share_amount": "500",
        "from_currency": "1",
        "icon_id": "1",
        "recur_id": "200000"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide valid recurring frequency id.'

def test_split_expenses_successed(client):
    split_expenses_data = {
        "groupId": "1",
        "amount": "1234441"
    }

    json_data = json.dumps(split_expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/splitExpense', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 200
    assert data['expenses_per_ppl'] == '308610.25'

def test_split_expenses_without_group_id_failed(client):
    split_expenses_data = {
        "amount": "1234441"
    }

    json_data = json.dumps(split_expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/splitExpense', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Group ID not specified in the request'

def test_split_expenses_without_amount_failed(client):
    split_expenses_data = {
        "groupId": "1"
    }

    json_data = json.dumps(split_expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/splitExpense', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Amount are not specified in the request'






