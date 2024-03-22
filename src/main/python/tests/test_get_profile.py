import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from main import app
from flask import json
import pytest
from config.database_config import db
from utility.user_utility import User_Utility
from utility.friends_utility import Friends_Utility
from utility.groups_utility import Groups_Utility
from utility.grouping_utility import Grouping_Utility


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='function')
def init_db():
    """Initialize a clean database before each test."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db
        db.session.rollback()

@pytest.fixture(scope="function")
def setup():
    user_db = User_Utility()
    friends_db = Friends_Utility()
    groups_db = Groups_Utility()
    grouping_db = Grouping_Utility()
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
    friends_db.create(user_id=user1.get('user_id'), friend_id=user3.get('user_id'))
    group1, _ = groups_db.create(group_name='group1')
    group2, _ = groups_db.create(group_name='group2')
    grouping_db.create(group_id=group1.get('group_id'), user_id=user1.get('user_id'))
    grouping_db.create(group_id=group1.get('group_id'), user_id=user2.get('user_id'))
    grouping_db.create(group_id=group2.get('group_id'), user_id=user1.get('user_id'))
    grouping_db.create(group_id=group2.get('group_id'), user_id=user3.get('user_id'))
    yield user1
        
def test_get_profile_success(client, init_db, setup):
    user1 = setup
    response = client.get('/profile/' + str(user1.get('user_id')))
    assert response.status_code == 200

    data = json.loads(response.data)
    print(data)

    user = data['user']
    assert user['user_name'] == user1['user_name']
    assert user['email'] == user1['email']
    assert user['password'] == user1['password']
    assert user['first_name'] == user1['first_name']
    assert user['last_name'] == user1['last_name']
    assert user['bio'] == ''

    friends = data['friends']
    assert len(friends) == 2

    groups = data['groups']
    assert len(groups) == 2