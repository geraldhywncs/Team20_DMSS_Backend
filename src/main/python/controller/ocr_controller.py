import cv2
import pytesseract
import numpy as np
import re
from skimage.filters import threshold_local
from flask import request, jsonify
from utility.ocr_utility import OCR_Utility

class OCR_Controller:
    def __init__(self, app):
        self.app = app


        @app.route('/ocr', methods=['POST'])
        def run_ocr():
            print('ocr called!')
            if 'image' not in request.files:
                return jsonify({'error': 'No image provided'}), 400

            image_file = request.files['image']

            img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

            extracted_amount = OCR_Utility.ocr_process(img)
            print(extracted_amount)

            # cleaned_text = OCR_Utility.clean_text(extracted_text)
            # print(cleaned_text)
            
            if extracted_amount and re.match(r'^\d+(\.\d{1,2})?$', extracted_amount):
                return jsonify(response =float(extracted_amount), ocr_status_code=200)
            else:
                return jsonify(response=extracted_amount,ocr_status_code=400), 400

            # return jsonify( receipt_amount = cleaned_text)

