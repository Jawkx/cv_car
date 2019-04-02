import cv2
import numpy as np

img = cv2.imread('temptest/temptest.jpg',0)
ret,thresh1 = cv2.threshold(img,30,255,cv2.THRESH_BINARY)

cv2.imshow('test',thresh1)

cv2.waitKey(0)
