import picamera
import picamera.array
import time
import cv2
import cv2.cv as cv
import numpy as np
import smbus
import math
import RPi.GPIO as GPIO

lower_purple = np.array([109,102,55])
upper_purple = np.array([143,188,216])

camera = picamera.PiCamera()
camera.resolution = (560,256)
camera.framerate = 60
rawCapture = picamera.array.PiRGBArray(camera)

for frame in camera.capture_continuous(rawCapture,format='bgr',use_video_port=True):

	img = rawCapture.array
	maskedpurple = cv2.inRange(hsv,lower_purple,upper_purple)

	cv2.imshow( "purpleonly" , maskedpurple)

	rawCapture.truncate(0)

	if key==ord('q'):
		sendInt( 0 , car_address )
		GPIO.cleanup();
		break