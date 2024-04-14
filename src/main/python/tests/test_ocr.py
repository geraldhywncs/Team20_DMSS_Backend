import os
import pytest
from flask import json
from main import app  # Assuming your Flask app instance is named 'app'
from utility.ocr_utility import OCR_Utility


# @pytest.fixture(scope='function')

def test_run_ocr_success(client):
    success_image = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_image.jpg')
    with open(success_image, 'rb') as image_file:
        response = client.post('/ocr', data={'image': image_file})

    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'receipt_amount' in data
    assert 'receipt_text' in data

def test_run_ocr_no_image_provided(client):
    response = client.post('/ocr')

    assert response.status_code == 400
    assert 'error' in response.json

def test_run_ocr_junk_image_provided(client):
    junk_image = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'junk_image.jpg')

    with open(junk_image, 'rb') as image_file:
        response = client.post('/ocr', data={'image': image_file})

    data = json.loads(response.data)
    assert response.status_code == 400
    assert 'Unable to perform OCR on image' in data['response']
    assert 'receipt_amount' not in data
    assert 'receipt_text' not in data