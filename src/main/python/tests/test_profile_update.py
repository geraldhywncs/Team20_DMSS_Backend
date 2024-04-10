from flask import json
import pytest
from utility.user_utility import User_Utility

@pytest.fixture(scope="function")
def setup():
    user_db = User_Utility()
    user1, _ = user_db.create(
        user_name="user1", 
        email="user1@example.com", 
        password="password", 
        first_name="user", 
        last_name="1"
    )
    yield user1
        
def test_update_profile_success(client, init_db, setup):
    user1 = setup
    data = {'user_details': {
        'first_name': 'John', 
        'last_name': 'Doe', 
        'user_name': 'johndoe', 
        'bio': 'I am john doe.'
    }}
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    response = client.put('/user/' + str(user1.get('user_id')), data=json_data, headers=headers)
    assert response.status_code == 200

    data = json.loads(response.data)

    user = data['user']
    assert user['user_name'] == 'johndoe'
    assert user['email'] == user1['email']
    assert user['password'] == user1['password']
    assert user['first_name'] == 'John'
    assert user['last_name'] == 'Doe'
    assert user['bio'] == 'I am john doe.'