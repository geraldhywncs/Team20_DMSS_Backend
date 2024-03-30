import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from main import app
from flask import json
import pytest
from config.database_config import db
from model.user_model import User_Model
from model.category_model import Category_Model

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='function')
def init_db():
    """Initialize a clean database before each test."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db
        db.session.rollback()

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
        }
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
        "user_id":"5000"
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












