import cv2
import numpy as np

image = cv2.imread('parking.jpeg')
image_temp = image.copy()
cv2.imshow('Image', image)
cv2.waitKey(0)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
_, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    # if the contour is open
    rect = cv2.minAreaRect(c)    
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(image_temp, [box], 0, (0, 0, 0))

cv2.imshow('Parking Spaces Detected', image_temp)
cv2.waitKey(0)    

image_temp_gray = cv2.cvtColor(image_temp, cv2.COLOR_BGR2GRAY)
ret, thresh_temp = cv2.threshold(image_temp_gray, 200, 255, cv2.THRESH_BINARY_INV)
# kernel = np.ones((5,5), np.uint8)
dilation = cv2.dilate(thresh_temp, cv2.getStructuringElement(cv2.MORPH_RECT, (5,5)), iterations=1)
_, contours, hierarchy = cv2.findContours(dilation.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    a = cv2.contourArea(c, True)
    
    if a > 0: # If we have a parking space
        rect = cv2.minAreaRect(c)        
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        print(box)
        cv2.drawContours(image, [box], 0, (0, 255, 0))

cv2.imshow('Result', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
