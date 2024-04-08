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
    yield (user1, user2, user3)
        
def test_create_group_success(client, init_db, setup):
    user1, user2, user3 = setup
    headers = {'Content-Type': 'application/json'}

    json_data = json.dumps({
        'group_name': 'my group name', 
        'group_member_ids': [user1.get('user_id'), user2.get('user_id'), user3.get('user_id')]
        })
    response = client.post('/groups', data=json_data, headers=headers)
    assert response.status_code == 200

    data = json.loads(response.data)

    group = data['group']
    assert group.get('group_name') == 'my group name'
    
    group_members = data['group_members']
    assert len(group_members) == 3