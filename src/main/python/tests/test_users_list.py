from flask import json
import pytest
from utility.user_utility import User_Utility

@pytest.fixture(scope="function")
def setup():
    user_db = User_Utility()
    user_db.create(
        user_name="user1", 
        email="user1@example.com", 
        password="password", 
        first_name="user", 
        last_name="1"
    )
    user_db.create(
        user_name="user2", 
        email="user2@example.com", 
        password="password", 
        first_name="user", 
        last_name="2"
    )
    user_db.create(
        user_name="user3", 
        email="user3@example.com", 
        password="password", 
        first_name="user", 
        last_name="3"
    )
        
def test_list_users_success(client, init_db, setup):
    response = client.get('/users')
    assert response.status_code == 200

    data = json.loads(response.data)

    users = data['users']
    assert len(users) == 3