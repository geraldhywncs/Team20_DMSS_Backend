import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from main import app
from flask import json
import pytest
from config.database_config import db
from model.user_model import User_Model
from model.grouping_model import Grouping_Model
from model.groups_model import Groups_Model
from model.category_model import Category_Model
from model.currencies_model import Currencies_Model
from model.icon_model import Icon_Model
from model.recurring_frequency_model import Recurring_Frequency_Model

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
    # Insert data for users
    user_data = [
        ('Jun Jie', 'junjie.wee@ncs.com.sg', 'gAAAAABl7uZHcn6ltKCWubI_t3Wu5J96Awvz3Jr-dR0dZ3YHrVV7MLlufoiATkek_eiA35SMyBeG0T76isaAgngQ4HagUN_lrg=='),
        ('Gerald', 'gerald.hoo@ncs.com.sg', 'gAAAAABl7uZHcn6ltKCWubI_t3Wu5J96Awvz3Jr-dR0dZ3YHrVV7MLlufoiATkek_eiA35SMyBeG0T76isaAgngQ4HagUN_lrg=='),
        ('Wei Zee', 'weizee@ncs.com.sg', 'gAAAAABl7uZHcn6ltKCWubI_t3Wu5J96Awvz3Jr-dR0dZ3YHrVV7MLlufoiATkek_eiA35SMyBeG0T76isaAgngQ4HagUN_lrg==')
    ]
    for user_name, email, password in user_data:
        user_model = User_Model(
            user_name=user_name,
            email=email,
            password=password
        )
        db.session.add(user_model)

    # Insert data for groups
    group_data = [
        ('Japan Travel'),
        ('Korea Travel'),
        ('Gym'),
        ('Japan Travel'),
        ('Korea Travel'),
        ('Gym')
    ]
    for group_name in group_data:
        group_model = Groups_Model(
            group_name=group_name
        )
        db.session.add(group_model)

    # Insert data for userGrouping
    user_grouping_data = [
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 1),
        (2, 2),
        (3, 1),
        (3, 2),
        (4, 1)
    ]
    for group_id, user_id in user_grouping_data:
        user_grouping_model = Grouping_Model(
            group_id=group_id,
            user_id=user_id
        )
        db.session.add(user_grouping_model)

    # Insert data for categories
    category_data = [
        ('Food', 1),
        ('Travelling', 1),
        ('Rental', 1),
        ('Food', 2),
        ('Travelling', 2),
        ('Rental', 2)
    ]
    for category_name, user_id in category_data:
        category_model = Category_Model(
            category_name=category_name,
            user_id=user_id
        )
        db.session.add(category_model)

    # Insert data for currencies
    currency_data = [
        ('MXN', 'Mexican Peso'),
        ('SGD', 'Singapore Dollar'),
        ('HKD', 'Hong Kong Dollar'),
        ('KRW', 'South Korean Won'),
        ('TRY', 'Turkish Lira'),
        ('IDR', 'Indonesian Rupiah'),
        ('PHP', 'Philippine Peso'),
        ('THB', 'Thai Baht'),
        ('MYR', 'Malaysian Ringgit'),
        ('NOK', 'Norwegian Krone'),
        ('DKK', 'Danish Krone'),
        ('PLN', 'Polish Złoty'),
        ('HUF', 'Hungarian Forint'),
        ('CZK', 'Czech Koruna'),
        ('USD', 'United States Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound Sterling'),
        ('JPY', 'Japanese Yen'),
        ('AUD', 'Australian Dollar'),
        ('CAD', 'Canadian Dollar'),
        ('CHF', 'Swiss Franc'),
        ('CNY', 'Chinese Yuan'),
        ('SEK', 'Swedish Krona'),
        ('NZD', 'New Zealand Dollar'),
        ('INR', 'Indian Rupee'),
        ('BRL', 'Brazilian Real'),
        ('ZAR', 'South African Rand')
    ]
    for code, name in currency_data:
        currency_model = Currencies_Model(
            code=code,
            name=name
        )
        db.session.add(currency_model)

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

    # Insert data for recurring_frequency
    recurring_frequency_data = [
        ('Daily'),
        ('Weekly'),
        ('Monthly'),
        ('Yearly')
    ]
    for recur_name in recurring_frequency_data:
        recurring_model = Recurring_Frequency_Model(
            recur_name=recur_name
        )
        db.session.add(recurring_model)

    db.session.commit()
    yield

def test_create_expenses_successed(client, init_db, setup):
    expenses_data = {
        "user_id": "1",
        "group_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "share_amount": "500",
        "from_currency": "1",
        "icon_id": "1",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 200
    assert data['message'] == 'Transaction created successfully!'

def test_create_expenses_without_group_id_recur_id_successed(client):
    expenses_data = {
        "user_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "share_amount": "500",
        "from_currency": "1",
        "icon_id": "1",
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 200
    assert data['message'] == 'Transaction created successfully!'
    
def test_create_expenses_no_user_id_pass_failed(client):
    expenses_data = {
        "group_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "share_amount": "500",
        "from_currency": "1",
        "icon_id": "1",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide user id.'

def test_create_expenses_no_cat_id_pass_failed(client):
    expenses_data = {
        "user_id": "1",
        "group_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "share_amount": "500",
        "from_currency": "1",
        "icon_id": "1",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide category id.'

def test_create_expenses_no_title_pass_failed(client):
    expenses_data = {
        "user_id": "1",
        "group_id": "1",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "share_amount": "500",
        "from_currency": "1",
        "icon_id": "1",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide title.'

def test_create_expenses_no_share_amount_pass_failed(client):
    expenses_data = {
        "user_id": "1",
        "group_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "from_currency": "1",
        "icon_id": "1",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide share amount.'

def test_create_expenses_no_from_currency_pass_failed(client):
    expenses_data = {
        "user_id": "1",
        "group_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "share_amount": "500",
        "icon_id": "1",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide from Currency.'

def test_create_expenses_no_icon_id_pass_failed(client):
    expenses_data = {
        "user_id": "1",
        "group_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "share_amount": "500",
        "from_currency": "1",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide icon id.'

def test_create_expenses_invalid_user_id_failed(client):
    expenses_data = {
        "user_id": "100000",
        "group_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "share_amount": "500",
        "from_currency": "1",
        "icon_id": "1",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide valid user id.'

def test_create_expenses_invalid_group_id_failed(client):
    expenses_data = {
        "user_id": "1",
        "group_id": "100000",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "share_amount": "500",
        "from_currency": "1",
        "icon_id": "1",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide valid group id.'

def test_create_expenses_invalid_cat_id_failed(client):
    expenses_data = {
        "user_id": "1",
        "group_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "100000",
        "share_amount": "500",
        "from_currency": "1",
        "icon_id": "1",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide valid category id.'

def test_create_expenses_invalid_from_currency_failed(client):
    expenses_data = {
        "user_id": "1",
        "group_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "share_amount": "500",
        "from_currency": "100000",
        "icon_id": "1",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide valid currency id.'

def test_create_expenses_invalid_icon_id_failed(client):
    expenses_data = {
        "user_id": "1",
        "group_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "share_amount": "500",
        "from_currency": "1",
        "icon_id": "100000",
        "recur_id": "2"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide valid icon id.'

def test_create_expenses_invalid_recur_id_failed(client):
    expenses_data = {
        "user_id": "1",
        "group_id": "1",
        "title": "Rental",
        "description": "Pay monthly rental",
        "cat_id": "1",
        "share_amount": "500",
        "from_currency": "1",
        "icon_id": "1",
        "recur_id": "200000"
    }

    json_data = json.dumps(expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/create', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Invalid request. Please provide valid recurring frequency id.'

def test_split_expenses_successed(client):
    split_expenses_data = {
        "groupId": "1",
        "amount": "1234441"
    }

    json_data = json.dumps(split_expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/splitExpense', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 200
    assert data['expenses_per_ppl'] == '308610.25'

def test_split_expenses_without_group_id_failed(client):
    split_expenses_data = {
        "amount": "1234441"
    }

    json_data = json.dumps(split_expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/splitExpense', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Group ID not specified in the request'

def test_split_expenses_without_amount_failed(client):
    split_expenses_data = {
        "groupId": "1"
    }

    json_data = json.dumps(split_expenses_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/expenses/splitExpense', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 400
    assert data['message'] == 'Amount are not specified in the request'






