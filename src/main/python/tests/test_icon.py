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

def test_read_all_icon_successed(client):
    data = {}

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/icon/readAllIcon', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)


    assert status_code == 200
    assert data['icons'] == [
        {
            "icon_id": 1,
            "icon_name": "commute"
        },
        {
            "icon_id": 2,
            "icon_name": "flight_takeoff"
        },
        {
            "icon_id": 3,
            "icon_name": "home"
        },
        {
            "icon_id": 4,
            "icon_name": "shopping_cart"
        },
        {
            "icon_id": 5,
            "icon_name": "sports_esports"
        },
        {
            "icon_id": 6,
            "icon_name": "restaurant"
        },
        {
            "icon_id": 7,
            "icon_name": "cake"
        },
        {
            "icon_id": 8,
            "icon_name": "cruelty_free"
        },
        {
            "icon_id": 9,
            "icon_name": "snowboarding"
        },
        {
            "icon_id": 10,
            "icon_name": "fitness_center"
        },
        {
            "icon_id": 11,
            "icon_name": "checkroom"
        }
    ]

def test_read_icon_successed(client):
    data = {"icon_id": 1}

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/icon/readAllIcon', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 200
    assert data['icon_id'] == 1
    assert data['icon_name'] == "commute"

def test_read_icon_invalid_icon_id_failed(client):
    data = {
        "icon_id": 1000
    }

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/icon/readAllIcon', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 404
    assert data["message"].startswith("Icon with ID")













