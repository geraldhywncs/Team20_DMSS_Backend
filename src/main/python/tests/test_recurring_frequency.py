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

def test_read_all_recurring_frequencies_successed(client):
    data = {}

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/recurringFrequency/readAllrecurringFrequencies', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)


    assert status_code == 200
    assert data['recurring_frequency'] == [
        {
            "recur_name": "Daily",
            "recurring_id": 1
        },
        {
            "recur_name": "Weekly",
            "recurring_id": 2
        },
        {
            "recur_name": "Monthly",
            "recurring_id": 3
        },
        {
            "recur_name": "Yearly",
            "recurring_id": 4
        }
    ]

def test_read_recurring_frequencies_successed(client):
    data = {"recurring_id": 1}

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/recurringFrequency/readAllrecurringFrequencies', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 200
    assert data['recur_name'] == "Daily"
    assert data['recurring_id'] == 1

def test_read_recurring_frequencies_invalid_recurring_id_failed(client):
    data = {
        "recurring_id": 1000
    }

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/recurringFrequency/readAllrecurringFrequencies', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 404
    assert data["message"].startswith("Recurring frequency with ID")













