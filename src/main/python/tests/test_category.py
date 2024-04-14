from flask import json
import pytest
from config.database_config import db
from model.user_model import User_Model
from model.category_model import Category_Model

@pytest.fixture(scope="function")
def setup():
    user_data = [
            ('Jun Jie', 'junjie.wee@ncs.com.sg', 'gAAAAABl7uZHcn6ltKCWubI_t3Wu5J96Awvz3Jr-dR0dZ3YHrVV7MLlufoiATkek_eiA35SMyBeG0T76isaAgngQ4HagUN_lrg=='),
            ('Gerald', 'gerald.hoo@ncs.com.sg', 'gAAAAABl7uZHcn6ltKCWubI_t3Wu5J96Awvz3Jr-dR0dZ3YHrVV7MLlufoiATkek_eiA35SMyBeG0T76isaAgngQ4HagUN_lrg=='),
            ('Wei Zee', 'weizee@ncs.com.sg', 'gAAAAABl7uZHcn6ltKCWubI_t3Wu5J96Awvz3Jr-dR0dZ3YHrVV7MLlufoiATkek_eiA35SMyBeG0T76isaAgngQ4HagUN_lrg==')
        ]
    category_data = [
            ('Food', 1),
            ('Travelling', 1),
            ('Rental', 1),
            ('Food', 2),
            ('Travelling', 2),
            ('Rental', 2)
        ]
    for user_name, email, password in user_data:
        user_model = User_Model(
            user_id=None,
            user_name=user_name,
            email=email,
            password=password,
            first_name=None,  
            last_name=None, 
            bio=None
        )
        db.session.add(user_model)

    for category_name, user_id in category_data:
        category_model = Category_Model(
            category_name=category_name,
            user_id=user_id
        )
        db.session.add(category_model)

    db.session.commit()
    yield category_data

def test_read_category_successed(client, init_db, setup):
    data = {"user_id":"1"}

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/category/readCategory', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert data['categories'] == [
        {
            "category_id": 1,
            "category_name": "Food",
            "user_id": 1
        },
        {
            "category_id": 2,
            "category_name": "Travelling",
            "user_id": 1
        },
        {
            "category_id": 3,
            "category_name": "Rental",
            "user_id": 1
        },
        
    ]
    assert status_code == 200

def test_read_category_without_user_id_success(client):
    data = {
    }

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/category/readCategory', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 200
    assert data["categories"] == [
        {
            "category_id": 1,
            "category_name": "Food",
            "user_id": 1
        },
        {
            "category_id": 2,
            "category_name": "Travelling",
            "user_id": 1
        },
        {
            "category_id": 3,
            "category_name": "Rental",
            "user_id": 1
        },
        {
            "category_id": 4,
            "category_name": "Food",
            "user_id": 2
        },
        {
            "category_id": 5,
            "category_name": "Travelling",
            "user_id": 2
        },
        {
            "category_id": 6,
            "category_name": "Rental",
            "user_id": 2
        }
    ]

def test_read_category_invalid_user_id_failed(client):
    data = {
        "user_id":123131
    }

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/category/readCategory', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 404
    assert data["message"].startswith("Category with user id")


def test_read_category_invalid_data_type(client, init_db, setup):
    data = {"user_id":"invalid"}

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/category/readCategory', data=json_data, headers=headers)

    status_code = response.status_code if not isinstance(response, tuple) else response[1]

    data = json.loads(response.data)

    assert status_code == 404 
    assert data["status_code"] == "404"
    assert "message" in data
def test_read_category_with_valid_user_id(client, init_db, setup):
    data = {"user_id":"1"}

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/category/readCategory', data=json_data, headers=headers)

    status_code = response.status_code if not isinstance(response, tuple) else response[1]

    data = json.loads(response.data)

    assert status_code == 200
    assert data["status_code"] == "200"
    assert "categories" in data

def test_read_category_with_invalid_user_id(client, init_db, setup):
    data = {"user_id":"5000"}

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/category/readCategory', data=json_data, headers=headers)

    status_code = response.status_code if not isinstance(response, tuple) else response[1]

    data = json.loads(response.data)

    assert status_code == 404
    assert data["status_code"] == "404"
    assert "message" in data

def test_add_category_with_valid_data(client, init_db, setup):
    data = {"category_name": "New Category", "user_id": "1"}

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/category/addCategory', data=json_data, headers=headers)

    status_code = response.status_code if not isinstance(response, tuple) else response[1]

    data = json.loads(response.data)

    assert status_code == int(data["status_code"]) 
    assert "message" in data

def test_delete_category_with_valid_data(client, init_db, setup):
    data = {"category_id": "1", "user_id": "1"}

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/category/deleteCategory', data=json_data, headers=headers)

    status_code = response.status_code if not isinstance(response, tuple) else response[1]

    data = json.loads(response.data)

    assert status_code == int(data["status_code"])
    assert "message" in data
def test_add_category_without_category_name(client, init_db, setup):
    data = {"user_id": "1"} 

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/category/addCategory', data=json_data, headers=headers)

    status_code = response.status_code if not isinstance(response, tuple) else response[1]

    data = json.loads(response.data)

    assert status_code == 400
    assert "error" in data 

def test_add_category_without_user_id(client, init_db, setup):
    data = {"category_name": "New Category"}  # Missing user_id

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/category/addCategory', data=json_data, headers=headers)

    status_code = response.status_code if not isinstance(response, tuple) else response[1]

    data = json.loads(response.data)

    assert status_code == 400
    assert "error" in data  
def test_delete_category_without_category_id(client, init_db, setup):
    data = {"user_id": "1"}  

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/category/deleteCategory', data=json_data, headers=headers)

    status_code = response.status_code if not isinstance(response, tuple) else response[1]

    data = json.loads(response.data)

    assert status_code == 400
    assert "error" in data  

def test_delete_category_without_user_id(client, init_db, setup):
    data = {"category_id": "1"}  

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/category/deleteCategory', data=json_data, headers=headers)

    status_code = response.status_code if not isinstance(response, tuple) else response[1]

    data = json.loads(response.data)

    assert status_code == 400
    assert "error" in data

def test_add_category_with_existing_category(client, init_db, setup):
    data = {"category_name": "Food", "user_id": "1"} 
    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/category/addCategory', data=json_data, headers=headers)

    status_code = response.status_code if not isinstance(response, tuple) else response[1]

    data = json.loads(response.data)

    assert status_code == 409 
    assert "error" in data

def test_delete_category_with_non_existent_category(client, init_db, setup):
    data = {"category_id": "5000", "user_id": "1"}  
    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/category/deleteCategory', data=json_data, headers=headers)

    status_code = response.status_code if not isinstance(response, tuple) else response[1]

    data = json.loads(response.data)

    assert status_code == 404
    assert "error" in data


def test_add_category_with_empty_category_name(client, init_db, setup):
    data = {"category_name": "", "user_id": "1"} 
    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/category/addCategory', data=json_data, headers=headers)

    status_code = response.status_code if not isinstance(response, tuple) else response[1]

    data = json.loads(response.data)

    assert status_code == 400  
    assert "error" in data

def test_delete_category_with_invalid_category_id(client, init_db, setup):
    data = {"category_id": "invalid", "user_id": "1"}

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/category/deleteCategory', data=json_data, headers=headers)

    status_code = response.status_code if not isinstance(response, tuple) else response[1]

    data = json.loads(response.data)

    assert status_code == 404
    assert "error" in data
