import cv2
import numpy as np

im = cv2.imread("parking.jpeg")
image_temp = im.copy()

gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
_, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

for i, c, in enumerate(contours):
    # if the contour is open
    
    if hierarchy[0][i][2] < 0:        
        x, y, w, h = cv2.boundingRect(c)
        # Draw a black line arround parking spaces
        cv2.rectangle(image_temp, (x, y), (x+w, y+h), (0,0,0), 2)

cv2.imshow('Parking Spaces Detected', image_temp)
cv2.waitKey(0)    

image_temp_gray = cv2.cvtColor(image_temp, cv2.COLOR_BGR2GRAY)
ret, thresh_temp = cv2.threshold(image_temp_gray, 200, 255, cv2.THRESH_BINARY_INV)
# kernel = np.ones((5,5), np.uint8)
dilation = cv2.dilate(thresh_temp, cv2.getStructuringElement(cv2.MORPH_RECT, (5,5)), iterations=1)
_, contours, hierarchy = cv2.findContours(dilation.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
cv2.imshow('image_temp_gray', image_temp_gray)
cv2.waitKey(0)


#gray = cv2.cvtColor(image_temp_gray, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(image_temp_gray, (5, 5), 0)
_, bina = cv2.threshold(gray,200,255,1) # inverted threshold (light obj on dark bg)
bina = cv2.dilate(bina, None)  # fill some holes
bina = cv2.dilate(bina, None)
bina = cv2.erode(bina, None)   # dilate made our shape larger, revert that
bina = cv2.erode(bina, None)
bina, contours, hierarchy = cv2.findContours(bina, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

rc = cv2.minAreaRect(contours[0])
box = cv2.boxPoints(rc)
print(box)
list_pt = []
for p in box:
    pt = (p[0],p[1])
    list_pt.append(pt)
    print(pt)
    cv2.circle(im,pt,5,(200,0,0),2)

box = np.int0(box)
cv2.drawContours(im, [box], 0, (0, 255, 0), 3)
cv2.imshow("plank", im)
cv2.waitKey(0)
cv2.destroyAllWindows()
