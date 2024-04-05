import cv2
import pytesseract
import numpy as np
from skimage.filters import threshold_local
import re


class OCR_Utility:
    def ocr_process(img):
        # To resize if image too large
        def opencv_resize(image, ratio):
            width = int(image.shape[1] * ratio)
            height = int(image.shape[0] * ratio)
            dim = (width, height)
            return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

        def approximate_contour(contour):
            peri = cv2.arcLength(contour, True)
            return cv2.approxPolyDP(contour, 0.032 * peri, True)

        def get_receipt_contour(contours):
            for c in contours:
                approx = approximate_contour(c)
                if len(approx) == 4:
                    return approx

        # Downscale image for processing efficiency
        resize = 500 / img.shape[0]
        original = img.copy()
        img = opencv_resize(img, resize)

        # Process image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        dilated = cv2.dilate(blurred, rectKernel)
        edged = cv2.Canny(dilated, 100, 200, apertureSize=3)
        contours, hierarchy = cv2.findContours(
            edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        largest_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        receipt_contour = get_receipt_contour(largest_contours)

        #rectangle
        def contour_to_rect(contour):
            pts = contour.reshape(4, 2)
            rect = np.zeros((4, 2), dtype="float32")

            s = pts.sum(axis=1)
            rect[0] = pts[np.argmin(s)]
            rect[2] = pts[np.argmax(s)]

            diff = np.diff(pts, axis=1)
            rect[1] = pts[np.argmin(diff)]
            rect[3] = pts[np.argmax(diff)]
            return rect / resize

        def wrap_perspective(img, rect):
            # adjust persepective
            (tl, tr, br, bl) = rect
            widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
            widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
            heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
            heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

            maxWidth = max(int(widthA), int(widthB))
            maxHeight = max(int(heightA), int(heightB))
            dst = np.array(
                [
                    [0, 0],
                    [maxWidth - 1, 0],
                    [maxWidth - 1, maxHeight - 1],
                    [0, maxHeight - 1],
                ],
                dtype="float32",
            )
            M = cv2.getPerspectiveTransform(rect, dst)
            return cv2.warpPerspective(img, M, (maxWidth, maxHeight))

        def bw_scanner(image):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            T = threshold_local(gray, 21, offset=10, method="gaussian")
            return (gray > T).astype("uint8") * 255

        scanned = wrap_perspective(original.copy(), contour_to_rect(receipt_contour))

        # Use pytesseract to extract text from the image
        result = bw_scanner(scanned)
        outputText = pytesseract.image_to_string(result)

        print("detected output text: " + outputText)

        amount_patterns = [
            r'(?:total|amount|due).*?([+-]?\d+(?:\.\d+)?)',
            r'(?<=total|amount|due|balance).*?([+-]?\d+(?:\.\d+)?)',
        # Add more patterns as needed
        ]

        final_amount = None
        for pattern in amount_patterns:
            match = re.search(pattern, outputText, re.IGNORECASE)
            if match:
                final_amount = match.group(1)
                break

        return final_amount
