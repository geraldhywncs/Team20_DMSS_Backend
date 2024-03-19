import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from main import app
from flask import json
import pytest


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_create_user(client):
    user_data = {
        'user_name': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword',
        'account_status': 'active'
    }

    # Send POST request to create user
    response = client.post('/users', data=user_data)
    assert response.status_code == 201

    data = json.loads(response.data)
    assert data['message'] == 'User created successfully'

    created_user = data['user']
    assert created_user['user_name'] == user_data['user_name']
    assert created_user['email'] == user_data['email']
    assert created_user['password'] == user_data['password']
    assert created_user['account_status'] == user_data['account_status']