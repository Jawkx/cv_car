#import picamera
#import picamera.array
import time
import cv2
#import cv2.cv as cv
import numpy as np

#camera = picamera.PiCamera()
#camera.resolution = (560,256)
#camera.framerate = 60

lower_bgreen = np.array([60,102,135])
upper_bgreen = np.array([90,255,255])

lower_bred = np.array([166,100,150]) 
upper_bred = np.array([175,255,255]) 

def watchtraffic(target)
	img = cv2.imread('tfc2.jpg',1)

	blurred = cv2.GaussianBlur(img, (9, 9), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)


	maskedbgreen = cv2.inRange(hsv,lower_bgreen,upper_bgreen)
	bgreencontours, _ = cv2.findContours(maskedbgreen,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

	maskedbred = cv2.inRange(hsv,lower_bred,upper_bred)
	bredcontours, _ = cv2.findContours(maskedbred,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

	if len(bgreencontours) != 0:
	    c = max(bgreencontours, key = cv2.contourArea)

	    green_area = cv2.contourArea(c) 
	else:
		green_area = 0

	if len(bredcontours) != 0:
	    c = max(bredcontours, key = cv2.contourArea)
	    red_area = cv2.contourArea(c)
	else:
		red_area = 0

	if red_area > green_area :
		return red
	elif green_area > red_area:
		return green

cv2.waitKey(0)