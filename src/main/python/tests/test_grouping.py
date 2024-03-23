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

def test_read_count_grouping_successed(client):
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
            "grouping_id": 4,
            "user_id": 1
        },
        {
            "group_id": 3,
            "group_name": "Gym",
            "grouping_id": 6,
            "user_id": 1
        },
        {
            "group_id": 4,
            "group_name": "Japan Travel",
            "grouping_id": 8,
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










