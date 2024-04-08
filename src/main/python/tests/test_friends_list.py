from flask import json
import pytest
from utility.user_utility import User_Utility
from utility.friends_utility import Friends_Utility

@pytest.fixture(scope="function")
def setup():
    user_db = User_Utility()
    friends_db = Friends_Utility()
    user1, _ = user_db.create(
        user_name="user1", 
        email="user1@example.com", 
        password="password", 
        first_name="user", 
        last_name="1"
    )
    user2, _ = user_db.create(
        user_name="user2", 
        email="user2@example.com", 
        password="password", 
        first_name="user", 
        last_name="2"
    )
    user3, _ = user_db.create(
        user_name="user3", 
        email="user3@example.com", 
        password="password", 
        first_name="user", 
        last_name="3"
    )
    friends_db.create(user_id=user1.get('user_id'), friend_id=user2.get('user_id'))
    friends_db.create(user_id=user2.get('user_id'), friend_id=user1.get('user_id'))
    friends_db.create(user_id=user2.get('user_id'), friend_id=user3.get('user_id'))
    friends_db.create(user_id=user3.get('user_id'), friend_id=user2.get('user_id'))
    yield (user1, user2, user3)
        
def test_get_friends_success(client, init_db, setup):
    user1, user2, user3 = setup

    # test user1
    response = client.get('/friends/' + str(user1.get('user_id')))
    assert response.status_code == 200

    data = json.loads(response.data)

    friends = data['friends']
    assert len(friends) == 1

    # test user2
    response = client.get('/friends/' + str(user2.get('user_id')))
    assert response.status_code == 200

    data = json.loads(response.data)

    friends = data['friends']
    assert len(friends) == 2

    # test user3
    response = client.get('/friends/' + str(user3.get('user_id')))
    assert response.status_code == 200

    data = json.loads(response.data)

    friends = data['friends']
    assert len(friends) == 1