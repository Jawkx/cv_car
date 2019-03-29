##IMPORT LIBRARY
import picamera
import picamera.array
import time
import cv2
import cv2.cv as cv
import numpy as np
import smbus
import math
import RPi.GPIO as GPIO

##SETTING FOR SERVO CONTROL AND ULTRASONIC
GPIO.setmode(GPIO.BCM)
servoPin = 17
trigger = 21 
echo = 20  


GPIO.setup(servoPin, GPIO.OUT)
GPIO.setup(trigger,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)
p = GPIO.PWM(servoPin, 50) # GPIO 17 for PWM with 50Hz
p.start(2.3) # Initialization

##SETTING FOR I2C
bus = smbus.SMBus(1)
car_address = 0x04

##GENERAL VARIABLE
action = 0

##VARIABLE FOR TEMPLATE RECOGNITION
i = 0
j = 0
array_draw_color = [ (255,0,0) , (0,255,0) , (0,0,255) , (0,255,255)]

tgoal0 = cv2.imread('t_goalpost/0.jpg',0)
tgoal1 = cv2.imread('t_goalpost/1.jpg',0)
tgoal2 = cv2.imread('t_goalpost/2.jpg',0)

trdd0 =  cv2.imread('t_rdd/0.jpg',0)
trdd1 =  cv2.imread('t_rdd/1.jpg',0)
trdd2 =  cv2.imread('t_rdd/2.jpg',0)

tcshape0 = cv2.imread('t_cshape/0.jpg',0)
tcshape1 = cv2.imread('t_cshape/1.jpg',0)
tcshape2 = cv2.imread('t_cshape/2.jpg',0)

goal_array_name = [ tgoal0 , tgoal1 , tgoal2 , 'goal']
rdd_array_name = [ trdd0 , trdd1 , trdd2 , 'read distance']
cshape_array_name = [ tcshape0 , tcshape1 , tcshape2 , 'countshape']

match_for_name = [goal_array_name , rdd_array_name , cshape_array_name ] 


##VAR FOR COLOR
lower_red = np.array([166,84,100]) 
upper_red = np.array([175,255,255]) 

lower_black = np.array([0,0,0])
upper_black = np.array([255,255,30])

lower_yellow = np.array([20,100,100])
upper_yellow = np.array([30,255,255])

lower_green = np.array([35,100,30])
upper_green = np.array([75,255,255])


##VAR FOR LINE FOLLOWING
lastcolor = 0
limitframe = 0
limitdelay = 10
lastcolorblack = 1
freeblack = 0
freeblackcount = 0
noblack = 0


matchingtemplate = 0
matchgoal = 0
i = 0

##INITIALIZE CAMERA
camera = picamera.PiCamera()
camera.resolution = (560,256)
camera.framerate = 60
rawCapture = picamera.array.PiRGBArray(camera)
sendstatus = input('Sendstatus 1-true 0-false:')
followblack = input('follow black 1-true 0 false :')
stop_distance = input('stop distance (cm):')

time.sleep(0.1)

def calculatedistance():

    GPIO.output(trigger, True)
 
    time.sleep(0.00001)
    GPIO.output(trigger, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    while GPIO.input(echo) == 0:
        StartTime = time.time()
 
    while GPIO.input(echo) == 1:
        StopTime = time.time()
 
    TimeElapsed = StopTime - StartTime
    distance = TimeElapsed/0.000058
 
    return distance

def sendInt(value,address):
		if ( sendstatus != 0 ):
			bus.write_byte(address, value)

    	return -1

def midpointCalc(target):
	x1 =((target[1][0])+(target[2][0]))/2
	y1 =((target[1][1])+(target[2][1]))/2
	x2 =((target[0][0])+(target[3][0]))/2
	y2 =((target[0][1])+(target[3][1]))/2

	x3 =((target[0][0])+(target[1][0]))/2
	y3 =((target[0][1])+(target[1][1]))/2
	x4 =((target[2][0])+(target[3][0]))/2
	y4 =((target[2][1])+(target[3][1]))/2
	
	l1 = (x2-x1)*(x2-x1) + (y2-y1)*(y2-y1)
	l2 = (x4-x3)*(x4-x3) + (y4-y3)*(y4-y3)

	if (l1 > l2) :
		absMidx = (x1+x2)/2
		absMidy = (y1+y2)/2
		return [x1,y1,x2,y2,absMidx,absMidy]
	elif( l2 > l1 ):
		absMidx = (x3+x4)/2
		absMidy = (y3+y4)/2

		return [x3,y3,x4,y4,absMidx,absMidy]

def countSendShift(contours):
	
	c = max(contours, key = cv2.contourArea)
	rect = cv2.minAreaRect(c)	
	box = cv.BoxPoints(rect)
	box = np.int0(box)
	cv2.drawContours(img,[box],0,(0,0,255))
	midpoint = midpointCalc(box)

	if midpoint != None :
		cv2.line(img,(midpoint[0],midpoint[1]),(midpoint[2],midpoint[3]),(255,0,0),3)
		cv2.circle(img,(midpoint[4],midpoint[5]),5,(0,255,0),-1)
		shift = midpoint[4] - 280;
				
		if ( sendstatus == 0 ):
			return 0
		elif( shift <= 140 and shift >= -140 ):
			return 1
		elif ( shift < -140):
			return 2
		elif( shift > 140 ):
			return 3
	else:
		return 4


for frame in camera.capture_continuous(rawCapture,format='bgr',use_video_port=True):

	img = rawCapture.array

	if ( action == 0 ): #linefollowing
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(img, (9, 9), 0)
		hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
		maskedred = cv2.inRange(hsv, lower_red, upper_red)
		maskedblack = cv2.inRange(hsv, lower_black , upper_black )
		maskedyellow = cv2.inRange(hsv, lower_yellow , upper_yellow )
		maskedgreen = cv2.inRange(hsv,lower_green,upper_green)
		blackcontours, _ = cv2.findContours(maskedblack,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
		redcontours, _ = cv2.findContours(maskedred,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)	
		yellowcontours, _ = cv2.findContours(maskedyellow,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)	
		greencontours, _ = cv2.findContours(maskedgreen,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
		circles = cv2.HoughCircles(gray,cv2.cv.CV_HOUGH_GRADIENT,1.5,100)

		if ( circles is not None ):
			action = 1	
		elif ( len( yellowcontours) != 0 ):

			if ( lastcolorblack == 1 ):
				noblack = 1
				lastcolorblack = 0
				limitdelay = 10
			
			
			if noblack == 1 :
				limitframe += 1
			sendInt( countSendShift(yellowcontours) , car_address )
		elif ( len( greencontours )!= 0 ):
		
			if ( lastcolorblack == 1 ):
				noblack = 1
				lastcolorblack = 0
				limitdelay = 20
				
			
			if noblack == 1 :
				limitframe += 1

			sendInt( countSendShift(greencontours) , car_address )
		elif ( len(redcontours) != 0 ):
		
			if ( lastcolorblack == 1 ):
				noblack = 1 
				lastcolorblack = 0
				limitdelay = 25
			

			
			if noblack == 1:
				limitframe += 1
				
			sendInt( countSendShift(redcontours) , car_address )		
		elif( len(blackcontours) != 0 and noblack!=1 ):
		
			if ( freeblack == 1 ):
				freeblackcount+= 1
			else:
				lastcolorblack = 1
			
			sendInt( countSendShift(blackcontours) , car_address )	
		else :
				sendInt(4)


		if ( limitframe >= limitdelay ):
			lastcolorblack = 0
			noblack = 0
			limitframe = 0
			freeblack = 1
		
		if ( freeblackcount >= 20 ):
			freeblack = 0
			freeblackcount = 0
	elif (action == 1): #block finding
		sendInt(1) #stop the car
		time.sleep(0.5)
		distance = 1000
		while ( distance < stop_distance ):
			sendInt(5 , car_address )
			distance = calculatedistance()

		p.ChangeDutyCycle(5.7)
		sendInt(1 , car_address )
		time.sleep(0.5)
		action = 2
	elif (action == 2): #TemplateMatching
	

	cv2.imshow("color", img)
		
	key = cv2.waitKey(1) & 0xFF

	rawCapture.truncate(0)

	if key==ord('q'):
		sendInt(0)
		GPIO.cleanup();
		break