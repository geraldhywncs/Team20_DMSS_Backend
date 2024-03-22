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

def test_read_all_currencies_successed(client):
    currency_data = {}

    json_data = json.dumps(currency_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/currency/readAllCurrencies', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 200
    assert data['currency'] == [
        {
            "code": "MXN",
            "currency_id": 1,
            "name": "Mexican Peso"
        },
        {
            "code": "SGD",
            "currency_id": 2,
            "name": "Singapore Dollar"
        },
        {
            "code": "HKD",
            "currency_id": 3,
            "name": "Hong Kong Dollar"
        },
        {
            "code": "KRW",
            "currency_id": 4,
            "name": "South Korean Won"
        },
        {
            "code": "TRY",
            "currency_id": 5,
            "name": "Turkish Lira"
        },
        {
            "code": "IDR",
            "currency_id": 6,
            "name": "Indonesian Rupiah"
        },
        {
            "code": "PHP",
            "currency_id": 7,
            "name": "Philippine Peso"
        },
        {
            "code": "THB",
            "currency_id": 8,
            "name": "Thai Baht"
        },
        {
            "code": "MYR",
            "currency_id": 9,
            "name": "Malaysian Ringgit"
        },
        {
            "code": "NOK",
            "currency_id": 10,
            "name": "Norwegian Krone"
        },
        {
            "code": "DKK",
            "currency_id": 11,
            "name": "Danish Krone"
        },
        {
            "code": "PLN",
            "currency_id": 12,
            "name": "Polish Złoty"
        },
        {
            "code": "HUF",
            "currency_id": 13,
            "name": "Hungarian Forint"
        },
        {
            "code": "CZK",
            "currency_id": 14,
            "name": "Czech Koruna"
        },
        {
            "code": "USD",
            "currency_id": 15,
            "name": "United States Dollar"
        },
        {
            "code": "EUR",
            "currency_id": 16,
            "name": "Euro"
        },
        {
            "code": "GBP",
            "currency_id": 17,
            "name": "British Pound Sterling"
        },
        {
            "code": "JPY",
            "currency_id": 18,
            "name": "Japanese Yen"
        },
        {
            "code": "AUD",
            "currency_id": 19,
            "name": "Australian Dollar"
        },
        {
            "code": "CAD",
            "currency_id": 20,
            "name": "Canadian Dollar"
        },
        {
            "code": "CHF",
            "currency_id": 21,
            "name": "Swiss Franc"
        },
        {
            "code": "CNY",
            "currency_id": 22,
            "name": "Chinese Yuan"
        },
        {
            "code": "SEK",
            "currency_id": 23,
            "name": "Swedish Krona"
        },
        {
            "code": "NZD",
            "currency_id": 24,
            "name": "New Zealand Dollar"
        },
        {
            "code": "INR",
            "currency_id": 25,
            "name": "Indian Rupee"
        },
        {
            "code": "BRL",
            "currency_id": 26,
            "name": "Brazilian Real"
        },
        {
            "code": "ZAR",
            "currency_id": 27,
            "name": "South African Rand"
        }
    ]

def test_read_currencies_successed(client):
    currency_data = {
        "currencyId":"1"
    }

    json_data = json.dumps(currency_data)

    headers = {'Content-Type': 'application/json'}

    response = client.post('/currency/readAllCurrencies', data=json_data, headers=headers)

    if isinstance(response, tuple):
        response, status_code = response
    else:
        status_code = response.status_code

    data = json.loads(response.data)

    assert status_code == 200
    assert data["code"] == "MXN"
    assert data["currency_id"] == 1
    assert data["name"] == "Mexican Peso"
    assert data["status_code"] == "200"









