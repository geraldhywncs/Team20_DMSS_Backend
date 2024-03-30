# import cv2
# import pytesseract
# import numpy as np
# from skimage.filters import threshold_local
from flask import request, jsonify
from utility.ocr_utility import OCR_Utility

class OCR_Controller:
    def __init__(self, app):
        self.app = app

        @app.route('/extract-text', methods=['POST'])
        def run_ocr():
            if 'image' not in request.files:
                return jsonify({'error': 'No image provided'}), 400

            image_file = request.files['image']

            img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

            # Perform OCR
            # extracted_text = self.perform_ocr(img)
            extracted_text = OCR_Utility.extract_text(img)

            # Clean output
            # cleaned_text = self.clean_extracted(extracted_text)

            # Return the extracted text
            return jsonify({'text': extracted_text})


    # def clean_extracted(self, img):
    #     cleaned_text = ''

    #     return jsonify({'text': extracted_text})
