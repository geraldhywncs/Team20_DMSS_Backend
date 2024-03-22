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

def test_read_category_successed(client):
    data = {"user_id":"1"}

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/category/readCategory', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 200
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

def test_read_category_without_user_id_failed(client):
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

    assert status_code == 404
    assert data["message"] == "User id is not provided"

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












