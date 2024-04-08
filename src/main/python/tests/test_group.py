from flask import json
import pytest
from config.database_config import db
from model.groups_model import Groups_Model

@pytest.fixture(scope="function")
def setup():
    # Insert data for groups
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
    db.session.commit()
    yield
    

def test_read_all_group_successed(client,init_db,setup):
    currency_data = {}

    json_data = json.dumps(currency_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/groups/read', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 200
    assert data['groups'] == [
        {
            "group_id": 1,
            "group_name": "Japan Travel"
        },
        {
            "group_id": 2,
            "group_name": "Korea Travel"
        },
        {
            "group_id": 3,
            "group_name": "Gym"
        },
        {
            "group_id": 4,
            "group_name": "Japan Travel"
        },
        {
            "group_id": 5,
            "group_name": "Korea Travel"
        },
        {
            "group_id": 6,
            "group_name": "Gym"
        }
    ]

def test_read_groups_successed(client):
    currency_data = {
        "group_id":"1"
    }

    json_data = json.dumps(currency_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/groups/read', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 200
    assert data["groups"]["group_id"] == 1
    assert data["groups"]["group_name"] == "Japan Travel"









