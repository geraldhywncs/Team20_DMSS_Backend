# update root dir
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# import
from main import app
from flask import json
import pytest
from config.database_config import db
from utility.user_utility import User_Utility
from utility.groups_utility import Groups_Utility
from utility.grouping_utility import Grouping_Utility

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='function')
def init_db(request):
    """Initialize a clean database before each test."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db
        db.session.rollback()
        db.drop_all()

        # Add a finalizer to ensure teardown
        def fin():
            db.session.remove()
            db.drop_all()
        request.addfinalizer(fin)

@pytest.fixture(scope="function")
def setup():
    user_db = User_Utility()
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
    group, _ = groups_db.create(group_name="test group")
    grouping_db.create(group_id=group.get('group_id'), user_id=user1.get('user_id'))
    grouping_db.create(group_id=group.get('group_id'), user_id=user2.get('user_id'))
    grouping_db.create(group_id=group.get('group_id'), user_id=user3.get('user_id'))
    yield (user1, user2, user3)
        
def test_list_groups_success(client, init_db, setup):
    user1, user2, user3 = setup

    # test user1
    response = client.get('/groups/' + str(user1.get('user_id')))
    assert response.status_code == 200

    data = json.loads(response.data)
    print(data)
    groups = data['groups']
    assert len(groups) == 1
    assert groups[0].get('group_name') == "test group"
    assert len(groups[0].get('members')) == 3

    # test user2
    response = client.get('/groups/' + str(user2.get('user_id')))
    assert response.status_code == 200

    data = json.loads(response.data)

    groups = data['groups']
    assert len(groups) == 1
    assert groups[0].get('group_name') == "test group"
    assert len(groups[0].get('members')) == 3

    # test user3
    response = client.get('/groups/' + str(user3.get('user_id')))
    assert response.status_code == 200

    data = json.loads(response.data)

    groups = data['groups']
    assert len(groups) == 1
    assert groups[0].get('group_name') == "test group"
    assert len(groups[0].get('members')) == 3