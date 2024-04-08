from flask import json
from config.database_config import db
import pytest
from model.recurring_frequency_model import Recurring_Frequency_Model

@pytest.fixture(scope="function")
def setup():
    # Insert data for icons
    recurring_frequency_data = [
        ('Daily'),
        ('Weekly'),
        ('Monthly'),
        ('Yearly')
    ]
    for recur_name in recurring_frequency_data:
        recurring_model = Recurring_Frequency_Model(
            recur_name=recur_name
        )
        db.session.add(recurring_model)
    db.session.commit()
    yield

def test_read_all_recurring_frequencies_successed(client, init_db, setup):
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













