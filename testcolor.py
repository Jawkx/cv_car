import picamera
import picamera.array
import time
import cv2
import cv2.cv as cv
import numpy as np
import smbus
import math
import RPi.GPIO as GPIO

lower_purple = np.array([0,123,120])
upper_purple = np.array([62,208,162])

camera = picamera.PiCamera()
camera.resolution = (560,256)
camera.framerate = 60
rawCapture = picamera.array.PiRGBArray(camera)

for frame in camera.capture_continuous(rawCapture,format='bgr',use_video_port=True):

	img = rawCapture.array
	hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	maskedpurple = cv2.inRange(img,lower_purple,upper_purple)
	contours , _ = cv2.findContours(maskedpurple,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

	if len(contours) > 10 :
		print('true')
	else :
		print ('false')
	cv2.imshow( "purpleonly" , img)

	rawCapture.truncate(0)
	key = cv2.waitKey(1) & 0xFF

	if key==ord('q'):
		break
