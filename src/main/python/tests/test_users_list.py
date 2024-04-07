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
from utility.friends_utility import Friends_Utility

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