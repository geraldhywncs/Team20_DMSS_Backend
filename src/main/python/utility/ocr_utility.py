import cv2
import pytesseract
import numpy as np
from skimage.filters import threshold_local
import re



class OCR_Utility:
    @staticmethod
    def ocr_process(img):
        def opencv_resize(image, ratio):
            width = int(image.shape[1] * ratio)
            height = int(image.shape[0] * ratio)
            dim = (width, height)
            return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

        def approximate_contour(contour):
            peri = cv2.arcLength(contour, True)
            return cv2.approxPolyDP(contour, 0.04 * peri, True)

        def get_receipt_contour(contours):
            for c in contours:
                approx = approximate_contour(c)
                if len(approx) == 4:
                    return approx

        #downscale image for processing efficiency
        resize = 800 / img.shape[0]
        original = img.copy()
        img = opencv_resize(img, resize)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 50, 150)

        # locates contours
        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        receipt_contour = get_receipt_contour(contours)

        # Perspective transformation
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

        def warp_perspective(img, rect):
            (tl, tr, br, bl) = rect
            widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
            widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
            maxWidth = max(int(widthA), int(widthB))
            heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
            heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
            maxHeight = max(int(heightA), int(heightB))
            dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype="float32")
            M = cv2.getPerspectiveTransform(rect, dst)
            return cv2.warpPerspective(img, M, (maxWidth, maxHeight))

        scanned = warp_perspective(original.copy(), contour_to_rect(receipt_contour))

        # Text extraction
        def bw_scanner(image):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            T = threshold_local(gray, 15, offset=8, method="gaussian")
            return (gray > T).astype("uint8") * 255

        result = bw_scanner(scanned)
        output_text = pytesseract.image_to_string(result)

        print("Detected output text: " + output_text)

        amount_patterns = [
            r'(?:total|amount|due).*?([+-]?\d+(?:\.\d+)?)',
            r'(?<=total|amount|due|balance).*?([+-]?\d+(?:\.\d+)?)',
            # Add more patterns as needed
        ]

        final_amount = None
        for pattern in amount_patterns:
            match = re.search(pattern, output_text, re.IGNORECASE)
            if match:
                final_amount = match.group(1)
                break

        return final_amount
