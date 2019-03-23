#code only for template matching
import picamera
import picamera.array
import time
import cv2
import cv2.cv as cv
import numpy as np
import time
import smbus
import time
import math
import RPi.GPIO as GPIO
import time

i = 0
j = 0

matching_name = "none"
matched = 0

array_draw_color = [ (255,0,0) , (0,255,0) , (0,0,255) , (0,255,255)]

tgoal0 = cv2.imread('template/_goalpost/0.jpg',0)
tgoal1 = cv2.imread('template/_goalpost/1.jpg',0)
tgoal2 = cv2.imread('template/_goalpost/2.jpg',0)

trdd0 =  cv2.imread('template/_rdd/0.jpg',0)
trdd1 =  cv2.imread('template/_rdd/1.jpg',0)
trdd2 =  cv2.imread('template/_rdd/2.jpg',0)

tcshape0 = cv2.imread('template/_cshape/0.jpg',0)
tcshape1 = cv2.imread('template/_cshape/1.jpg',0)
tcshape2 = cv2.imread('template/_cshape/2.jpg',0)

goal_array_name = [ tgoal0 , tgoal1 , tgoal2 , 'goal']
rdd_array_name = [ trdd0 , trdd1 , trdd2 , 'read distance']
cshape_array_name = [ tcshape0 , tcshape1 , tcshape2 , 'countshape']

match_for_name = [goal_array_name , rdd_array_name , cshape_array_name ]
thresholdValue = [ 0.7, 0.7 , 0.7 ]
img = cv.imread('temptest.jpg',0)
img_gray = cv2.cvtColor( img , cv2.COLOR_BGR2GRAY)

for i in range ( len(match_for_name) ):

	matching_name = match_for_name[i]

	for j in range ( len ( matching_name ) ):
		current_template = matching_name[j]
		res = cv2.matchTemplate(img_gray, current_template,cv2.TM_CCOEFF_NORMED)
		loc = np.where( res >= thresholdValue[j])


		if len( zip(*loc[::-1]) ) >= 3 :
			matched += 1
	
		for pt in zip(*loc[::-1]):
		   cv2.circle(img_rgb, pt, 5 ,array_draw_color[i] , -1 )

	
	j = 0

	if ( matched != 0 ):
		print(matchingname)
		break
	else :
		i = 0
		