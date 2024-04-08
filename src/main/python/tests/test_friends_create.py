from flask import json
import pytest
from utility.user_utility import User_Utility
from utility.friends_utility import Friends_Utility

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
    user2, _ = user_db.create(
        user_name="user2", 
        email="user2@example.com", 
        password="password", 
        first_name="user", 
        last_name="2"
    )
    yield (user1, user2)
        
def test_create_friends_success(client, init_db, setup):
    user1, user2 = setup
    headers = {'Content-Type': 'application/json'}
    friends_db = Friends_Utility()

    json_data = json.dumps({'friend_id': user2.get('user_id')})
    response = client.post('/friends/' + str(user1.get('user_id')), data=json_data, headers=headers)
    assert response.status_code == 200

    data = json.loads(response.data)

    friend = data['friend']
    assert friend.get('user_id') == user1.get('user_id')
    assert friend.get('friend_id') == user2.get('user_id')

    friendList1, _ = friends_db.list_by_user_id(user_id=user1.get('user_id'))
    assert len(friendList1) == 1
    friendList2, _ = friends_db.list_by_user_id(user_id=user2.get('user_id'))
    assert len(friendList2) == 0
