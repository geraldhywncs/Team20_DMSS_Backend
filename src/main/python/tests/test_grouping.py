import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from main import app
from flask import json
import pytest
from config.database_config import db
from model.grouping_model import Grouping_Model
from model.groups_model import Groups_Model
from model.user_model import User_Model

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='function')
def init_db(request):
    """Initialize a clean database before each test."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db
        db.session.rollback()
        db.drop_all()

        # Add a finalizer to ensure teardown
        def fin():
            db.session.remove()
            db.drop_all()
        request.addfinalizer(fin)

@pytest.fixture(scope="function")
def setup():
    group_data = [
        ('Japan Travel'),
        ('Korea Travel'),
        ('Gym'),
        ('Japan Travel'),
        ('Korea Travel'),
        ('Gym')
    ]
    for group_name in group_data:
        group_model = Groups_Model(
            group_name=group_name
        )
        db.session.add(group_model)

    # Insert data for userGrouping
    user_grouping_data = [
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 1),
        (2, 2),
        (3, 1),
        (3, 2),
        (4, 1)
    ]
    for group_id, user_id in user_grouping_data:
        user_grouping_model = Grouping_Model(
            group_id=group_id,
            user_id=user_id
        )
        db.session.add(user_grouping_model)

    user_data = [
        ('Jun Jie', 'junjie.wee@ncs.com.sg', 'gAAAAABl7uZHcn6ltKCWubI_t3Wu5J96Awvz3Jr-dR0dZ3YHrVV7MLlufoiATkek_eiA35SMyBeG0T76isaAgngQ4HagUN_lrg=='),
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
    db.session.commit()
    yield

def test_read_count_grouping_successed(client, init_db, setup):
    currency_data = {"group_id": "1"}

    json_data = json.dumps(currency_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/grouping/countUserGrouping', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 200
    assert data['total_user'] == 4

def test_read_count_grouping_without_group_id_failed(client):
    currency_data = {
    }

    json_data = json.dumps(currency_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/grouping/countUserGrouping', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 404
    assert data["message"] == "Group ID is not provided"

def test_read_all_grouping_successed(client):
    currency_data = {
        "user_id": "1"
    }

    json_data = json.dumps(currency_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/grouping/read', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 200
    assert data["grouping"] == [
        {
            "group_id": 1,
            "group_name": "Japan Travel",
            "grouping_id": 1,
            "user_id": 1
        },
        {
            "group_id": 2,
            "group_name": "Korea Travel",
            "grouping_id": 5,
            "user_id": 1
        },
        {
            "group_id": 3,
            "group_name": "Gym",
            "grouping_id": 7,
            "user_id": 1
        },
        {
            "group_id": 4,
            "group_name": "Japan Travel",
            "grouping_id": 9,
            "user_id": 1
        }
    ]

def test_read_all_grouping_without_user_id_failed(client):
    currency_data = {}

    json_data = json.dumps(currency_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/grouping/read', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data["message"] == "User ID is not provided"

def test_read_all_grouping_invalid_user_id_failed(client):
    currency_data = {"user_id": "100"}

    json_data = json.dumps(currency_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/grouping/read', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data["message"] == "Invalid request. Please provide valid user id."










