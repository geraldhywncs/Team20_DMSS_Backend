import cv2
import pytesseract
import numpy

from skimage.filters import threshold_local
from PIL import Image
from flask import Flask, request, jsonify

class OCR_Utility:
    # def __init__(self):
    #     self.ocr_utility = OCR_Utility()
    def extract_text(img):
        ###### Locate receipt in photo ######
        
        # To resize if image too large
        def opencv_resize(image, ratio):
            width = int(image.shape[1] * ratio)
            height = int(image.shape[0] * ratio)
            dim = (width, height)
            return cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

        ### Search for receipt in image ###
        # approximate the contour by a more primitive polygon shape
        def approximate_contour(contour):
            peri = cv2.arcLength(contour, True)
            return cv2.approxPolyDP(contour, 0.032 * peri, True)

        def get_receipt_contour(contours):    
            # loop over the contours
            for c in contours:
                approx = approximate_contour(c)
                # if our approximated contour has four points, we can assume it is receipt's rectangle
                if len(approx) == 4:
                    return approx


        # Path to the image file
        # image_path = 'Test_images\img4.jpg'
        # image_path = request.files['image']
        # image_path = img

        # Read the image using OpenCV

        # image = cv2.imdecode(numpy.frombuffer(image_path.read(), numpy.uint8), cv2.IMREAD_COLOR)
        image = img

        # Downscale image as finding receipt contour is more efficient on a small image
        resize = 500 / image.shape[0]
        original = image.copy()
        image = opencv_resize(image, resize)

        # # Resize the image to a smaller size
        # image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply a Gaussian blur to the image
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Detect white regions
        rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        dilated = cv2.dilate(blurred, rectKernel)

        # Detect edges
        edged = cv2.Canny(dilated, 100, 200, apertureSize=3)
        contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        image_with_contours = cv2.drawContours(image.copy(), contours, -1, (0,255,0), 3)

        largest_contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]

        receipt_contour = get_receipt_contour(largest_contours)


        ###### Locate receipt in photo ######

        def contour_to_rect(contour):
            pts = contour.reshape(4, 2)
            rect = numpy.zeros((4, 2), dtype = "float32")
            # top-left point has the smallest sum
            # bottom-right has the largest sum
            s = pts.sum(axis = 1)
            rect[0] = pts[numpy.argmin(s)]
            rect[2] = pts[numpy.argmax(s)]
            # compute the difference between the points:
            # the top-right will have the minumum difference 
            # the bottom-left will have the maximum difference
            diff = numpy.diff(pts, axis = 1)
            rect[1] = pts[numpy.argmin(diff)]
            rect[3] = pts[numpy.argmax(diff)]
            return rect / resize


        def wrap_perspective(img, rect):
            # unpack rectangle points: top left, top right, bottom right, bottom left
            (tl, tr, br, bl) = rect
            # compute the width of the new image
            widthA = numpy.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
            
            widthB = numpy.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
            # compute the height of the new image
            heightA = numpy.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
            heightB = numpy.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
            # take the maximum of the width and height values to reach
            # our final dimensions
            maxWidth = max(int(widthA), int(widthB))
            maxHeight = max(int(heightA), int(heightB))
            # destination points which will be used to map the screen to a "scanned" view
            dst = numpy.array([
                [0, 0],
                [maxWidth - 1, 0],
                [maxWidth - 1, maxHeight - 1],
                [0, maxHeight - 1]], dtype = "float32")
            # calculate the perspective transform matrix
            M = cv2.getPerspectiveTransform(rect, dst)
            # warp the perspective to grab the screen
            return cv2.warpPerspective(img, M, (maxWidth, maxHeight))


        def bw_scanner(image):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            T = threshold_local(gray, 21, offset = 10, method = "gaussian")
            return (gray > T).astype("uint8") * 255

        scanned = wrap_perspective(original.copy(), contour_to_rect(receipt_contour))


        # Use pytesseract to extract text from the image
        result = bw_scanner(scanned)
        outputText = pytesseract.image_to_string(result)

        # For testing

        print(outputText)
        output = Image.fromarray(scanned)
        output.save('result.png')

        ### TO DO: Process the extracted text



        return outputText

# if __name__ == '__main__':
#     app.run(debug=True)


    
## curl -X POST -F "image=@testImage.jpg" http://127.0.0.1:5000/extract-text
## curl -X POST -F "" http://127.0.0.1:5000/extract-text
