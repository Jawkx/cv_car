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

tangle0 = cv2.imread('template/t_angle/0.jpg',0)
tangle1 = cv2.imread('template/t_angle/1.jpg',0)
tangle2 = cv2.imread('template/t_angle/2.jpg',0)

tcolorblue0 = cv2.imread('template/t_colorblue/0.jpg',0)
tcolorblue1 = cv2.imread('template/t_colorblue/1.jpg',0)
tcolorblue2 = cv2.imread('template/t_colorblue/2.jpg',0)

tcolorgreen0 = cv2.imread('template/t_colorgreen/0.jpg',0)
tcolorgreen1 = cv2.imread('template/t_colorgreen/1.jpg',0)
tcolorgreen2 = cv2.imread('template/t_colorgreen/2.jpg',0)

tcolorred0 = cv2.imread('template/t_colorred/0.jpg',0)
tcolorred1 = cv2.imread('template/t_colorred/1.jpg',0)
tcolorred2 = cv2.imread('template/t_colorred/2.jpg',0)

tcoloryellow0 = cv2.imread('template/t_coloryellow/0.jpg',0)
tcoloryellow1 = cv2.imread('template/t_coloryellow/1.jpg',0)
tcoloryellow2 = cv2.imread('template/t_coloryellow/2.jpg',0)

tcshape0 = cv2.imread('template/t_cshape/0.jpg',0)
tcshape1 = cv2.imread('template/t_cshape/1.jpg',0)
tcshape2 = cv2.imread('template/t_cshape/2.jpg',0)

tgoalpost0 = cv2.imread('template/t_goalpost/0.jpg',0)
tgoalpost1 = cv2.imread('template/t_goalpost/1.jpg',0)
tgoalpost2 = cv2.imread('template/t_goalpost/2.jpg',0)

trdd0 =  cv2.imread('template/t_rdd/0.jpg',0)
trdd1 =  cv2.imread('template/t_rdd/1.jpg',0)
trdd2 =  cv2.imread('template/t_rdd/2.jpg',0)

ttfl0 =  cv2.imread('template/t_tfl/0.jpg',0)
ttfl1 =  cv2.imread('template/t_tfl/1.jpg',0)
ttfl2 =  cv2.imread('template/t_tfl/2.jpg',0)

angle_name = [ tangle0 , tangle1 , tangle2 , 'readangle']
colorblue_name = [ tcolorblue0 , tcolorblue1 , tcolorblue2 , 'follow blue']
colorgreen_name = [ tcolorgreen0 , tcolorgreen1 , tcolorgreen2 , 'follow green']
colorred_name = [tcolorred0 , tcolorred1 , tcolorred2 , 'followred']
coloryellow_name = [ tcoloryellow0 , tcoloryellow1 , tcoloryellow2 , 'follow yellow']
cshape_name = [ tcshape0 , tcshape1 , tcshape2 , 'countshape']
goal_name = [ tgoalpost0 , tgoalpost1 , tgoalpost2 , 'goal']
rdd_name = [ trdd0 , trdd1 , trdd2 , 'read distance']
tlf_name = [ ttfl0 , ttfl1 , ttfl2 , 'traffic light']

match_for_name = [ angle_name , colorblue_name , colorgreen_name , colorred_name , coloryellow_name , cshape_name , goal_name , rdd_name ,tlf_name]
thresholdValue = [ 0.8 , 0.8 , 0.8 , 0.7 , 0.8 , 0.9 , 0.8 , 0.9 , 0.5]

picture_to_read = input("Enter link for the picture to read:")

def readtemplate(target):
	matched = 0
	img = cv2.imread(target)
	img_gray = cv2.cvtColor( img , cv2.COLOR_BGR2GRAY)

	for i in range ( 0 , 8 ) :

		print("i=" , i)	
		for j in range ( 0, 3 ):
			print("j=",j)
			current_template = match_for_name[i][j]
			res = cv2.matchTemplate(img_gray, current_template,cv2.TM_CCOEFF_NORMED)
			loc = np.where( res >= thresholdValue[i])

			if len( zip(*loc[::-1]) ) >= 3 :
				matched = 1
		
			#for pt in zip(*loc[::-1]):
			#   cv2.circle(img, pt, 5 ,array_draw_color[i] , -1 )

		
		if ( matched != 0 ):
			return match_for_name[i][3]


	return "no match"

print(readtemplate(picture_to_read))



		