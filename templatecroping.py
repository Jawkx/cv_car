import cv2
import numpy as np

img = cv2.imread('temptest/temptest4.jpg',0)
blurred = cv2.GaussianBlur(img, (9, 9), 0)
ret,thresh = cv2.threshold(blurred,40,255,cv2.THRESH_BINARY_INV)
contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

c = max(contours, key = cv2.contourArea)
x,y,w,h = cv2.boundingRect(c)

cropped = img[ y:y+h , x:x+w ]
cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

resized = cv2.resize( cropped, (560,256) , interpolation = cv2.INTER_AREA)

'''
maskedblack = cv2.inRange(hsv, lower_black , upper_black )
blackcontours, _ = cv2.findContours(maskedblack,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

c = max(blackcontours, key = cv2.contourArea)
x,y,w,h = cv2.boundingRect(c)

cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

cv2.drawContours(img, blackcontours, -1, 255, 3)
#maskedwhite = cv2.inRange(hsv, lower_white , upper_white )
#whitecontours, _ = cv2.findContours(maskedblack,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

cv2.imshow('black',maskedblack)
cv2.imshow('img',img)
cv2.waitKey(0)
'''
cv2.imshow('resize',resized)
cv2.imshow('thresh',thresh)
cv2.imshow('cropped',cropped)
cv2.waitKey(0)