from flask import json
from config.database_config import db
import pytest
from model.icon_model import Icon_Model

@pytest.fixture(scope="function")
def setup():
    # Insert data for icons
    icon_data = [
        ('commute'),
        ('flight_takeoff'),
        ('home'),
        ('shopping_cart'),
        ('sports_esports'),
        ('restaurant'),
        ('cake'),
        ('cruelty_free'),
        ('snowboarding'),
        ('fitness_center'),
        ('checkroom')
    ]
    for icon_name in icon_data:
        icon_model = Icon_Model(
            icon_name=icon_name
        )
        db.session.add(icon_model)
    db.session.commit()
    yield

def test_read_all_icon_successed(client,init_db,setup):
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













