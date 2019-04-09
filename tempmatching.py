#code only for template - copy matching
import time
import cv2
import numpy as np
import math
import picamera
import picamera.array

i = 0
j = 0
matching_name = "none"

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

match_for_name = [ angle_name , colorblue_name , colorgreen_name , colorred_name , coloryellow_name , cshape_name , goal_name , rdd_name , tlf_name]
thresholdValue = [ 0.8 , 0.7 , 0.7 , 0.6 , 0.7 , 0.8 , 0.75 , 0.8 , 0.7]

def readtemplate(target):
	matched = 0
	for i in range ( 0 , 8 ) :

		print("i=" , i)	
		for j in range ( 0, 3 ):
			print("j=",j)
			current_template = match_for_name[i][j]
			res = cv2.matchTemplate(target, current_template,cv2.TM_CCOEFF_NORMED)
			loc = np.where( res >= thresholdValue[i])

			if len( zip(*loc[::-1]) ) >= 3 :
				matched = 1
		
			for pt in zip(*loc[::-1]):
			   cv2.circle(target, pt, 5 , (255,0,0) , -1 )
                
		if ( matched != 0 ):
			return match_for_name[i][3]


	return "no match"

camera = picamera.PiCamera()
camera.resolution = (560,256)
rawcapture = picamera.array.PiRGBArray(camera)
camera.capture(rawcapture,format='bgr')
img = rawcapture.array
blurred = cv2.GaussianBlur(img, (9, 9), 0)
gray = cv2.cvtColor(blurred,cv2.COLOR_BGR2GRAY)
print(readtemplate(gray))
#cv2.imshow("cropped",cropped)
#cv2.imshow('cropthresh',cropthresh)
#cv2.waitKey(0)
