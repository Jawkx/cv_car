#IMPORT LIBRARY
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
p.start(3.2) # Initialization

##SETTING FOR I2C
bus = smbus.SMBus(1)
car_address = 0x04
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
address = 0x68  

##GENERAL VARIABLE

##VARIABLE FOR TEMPLATE RECOGNITION
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

angle_name = [ tangle0 , tangle1 , tangle2 , 'readangle' , 3 ]
colorblue_name = [ tcolorblue0 , tcolorblue1 , tcolorblue2 , 'follow blue' , 0 ]
colorgreen_name = [ tcolorgreen0 , tcolorgreen1 , tcolorgreen2 , 'follow green' , 0 ]
colorred_name = [tcolorred0 , tcolorred1 , tcolorred2 , 'followred' , 0 ]
coloryellow_name = [ tcoloryellow0 , tcoloryellow1 , tcoloryellow2 , 'follow yellow' , 0]
cshape_name = [ tcshape0 , tcshape1 , tcshape2 , 'countshape' , 4 ]
goal_name = [ tgoalpost0 , tgoalpost1 , tgoalpost2 , 'goal' , 5 ]
rdd_name = [ trdd0 , trdd1 , trdd2 , 'read distance' , 6 ]
tlf_name = [ ttfl0 , ttfl1 , ttfl2 , 'traffic light' , 7 ]

match_for_name = [ angle_name , colorblue_name , colorgreen_name , colorred_name , coloryellow_name , cshape_name , goal_name , rdd_name , tlf_name ]
thresholdValue = [ 0.85 , 0.65 , 0.6 , 0.6 , 0.7 , 0.8 , 0.8 , 0.85 , 0.85]

##VAR FOR COLOR
lower_red = np.array([166,84,100]) 
upper_red = np.array([175,255,255]) 

lower_black = np.array([0,0,0])
upper_black = np.array([255,255,40])

lower_yellow = np.array([20,100,100])
upper_yellow = np.array([45,255,255])

lower_green = np.array([35,100,30])
upper_green = np.array([75,255,255])

lower_bgreen = np.array([60,102,135])
upper_bgreen = np.array([90,255,255])

lower_bred = np.array([166,100,150]) 
upper_bred = np.array([175,255,255]) 

lower_purple = np.array([120,60,70])
upper_purple = np.array([155,130,216])


##VAR FOR LINE FOLLOWING
lastcolor = 0
limitframe = 0
limitdelay = 10
limitdetectpurple = 0
limitdetectpurpleframe = 0
limitdetectpurpleframeval = 20
lastcolorblack = 1
freeblack = 0
freeblackcount = 0
noblack = 0

##VAR FOR ANGLE AND PREVIOUS ANGLE
current_angle = 0
highest_angle = 0

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

def readtemplate(target):
	matched = 0
	blurred = cv2.GaussianBlur(target,(9,9),0)
	img_gray = cv2.cvtColor( blurred , cv2.COLOR_BGR2GRAY)

	for i in range ( 0 , 9 ) :

		for j in range ( 0, 3 ):
			current_template = match_for_name[i][j]
			res = cv2.matchTemplate(img_gray, current_template,cv2.TM_CCOEFF_NORMED)
			loc = np.where( res >= thresholdValue[i])

			if len( zip(*loc[::-1]) ) >= 2 :
				matched = 1
		
		if ( matched != 0 ):
			return match_for_name[i][4]


	return 2

def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def get_angle():
    anglesum = 0
    for i in range (0,3):
	acceleration_xout = read_word_2c(0x3b)
	acceleration_yout = read_word_2c(0x3d)
	acceleration_zout = read_word_2c(0x3f)
	acceleration_xout_scaled = acceleration_xout / 16384.0
	acceleration_yout_scaled = acceleration_yout / 16384.0
	acceleration_zout_scaled = acceleration_zout / 16384.0

    	anglesum = anglesum + round(get_x_rotation(acceleration_xout_scaled, acceleration_yout_scaled, acceleration_zout_scaled)) 
	time.sleep(0.05)
    
    rawangle = anglesum/3
    if rawangle >= 0 :
	return rawangle
    elif rawangle < 0:
	return -rawangle

def countshape():
	print("countshape")
	p.ChangeDutyCycle(3.2) 
	time.sleep(1)

def watchtraffic(target):
	img = target

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
		return "red"
	elif green_area > red_area:
		return "green"

def findball(target):
	hsv = cv2.cvtColor(target,cv2.COLOR_BGR2HSV)
	maskedyellow = cv2.inRange(hsv, lower_yellow , upper_yellow )
	yellowcontours, _ = cv2.findContours(maskedyellow,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	if len(yellowcontours) != 0 :
		maxcontour = max( yellowcontours , key = cv2.contourArea )
		M = cv2.moments(maxcontour)
		#print "ball present"
		if  M["m00"] != 0:
			ballpoint =  int(M["m10"]/M["m00"])
			#print ballpoint
		
			ballshift = ballpoint - 280;
				
			if( ballshift <= 30 and ballshift >= -30 ):
				sendInt( 6 , car_address )
				time.sleep(0.2)
				sendInt( 0 , car_address )
				time.sleep(0.3)
                                p.ChangeDutyCycle(6.5)
				time.sleep ( 1 )
				print "middle"
                                return  9
			else:
				print "not middle"
				return 5
	else :
		return 5
	

def findbackline(target):
	hsv = cv2.cvtColor(target, cv2.COLOR_BGR2HSV)
	maskedred = cv2.inRange(hsv, lower_red, upper_red)
	maskedblack = cv2.inRange(hsv, lower_black , upper_black )
	maskedyellow = cv2.inRange(hsv, lower_yellow , upper_yellow )
	maskedgreen = cv2.inRange(hsv,lower_green,upper_green)
	blackcontours, _ = cv2.findContours(maskedblack,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	redcontours, _ = cv2.findContours(maskedred,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)	
	yellowcontours, _ = cv2.findContours(maskedyellow,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)	
	greencontours, _ = cv2.findContours(maskedgreen,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

	if blackcontours!=0 or redcontours!=0 or yellowcontours!=0 or greencontours!=0 :
		return  1
	else:
		return  0

def checkgp(target):
	hsv = cv2.cvtColor(target, cv2.COLOR_BGR2HSV)
	maskedgreen = cv2.inRange(hsv, lower_green , upper_green )
	greencontours, _ = cv2.findContours(maskedgreen,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

	if len(greencontours) != 0 :
		greenc = max(greencontours, key = cv2.contourArea)
		greenrect = cv2.minAreaRect(greenc)	
        	greenbox = cv.BoxPoints(greenrect)
		greenbox = np.int0(greenbox)
                cv2.drawContours(img,[greenbox],0,(0,0,255),2)
                if greenbox != None :
                    if ( greenbox[0][0] >= 250 and greenbox[1][0] <= 310 ):
                        print 'in goal'
			sendInt( 9 , car_address )
			time.sleep(1)
			sendInt( 0 , car_address )
			time.sleep(2)
			sendInt( 4 , car_address )
			p.ChangeDutyCycle(3.2)
			time.sleep(4)
			return 8
                    else :
                        print 'not in goal'
			return 9
        else :
            print 'no find green '
	    return 9

'''
----------------------------------------------------------------
================================================================
start program
================================================================
----------------------------------------------------------------
'''
##INITIALIZE CAMERA
camera = picamera.PiCamera()
camera.resolution = (560,256)
camera.framerate = 60
rawCapture = picamera.array.PiRGBArray(camera)
action = input('start at action:')
sendstatus = input('Sendstatus 1-true 0-false:')
stop_distance = 55
showimg = input('showimage:')

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture,format='bgr',use_video_port=True):

	img = rawCapture.array


	if ( action == 0 or action == 3 ): #linefollowing ang also readangle
		if ( action == 3 ):
			current_angle = get_angle()
    			print 'current_angle' , current_angle    
			print 'highest_angle' , highest_angle
			if current_angle > highest_angle :
				highest_angle = current_angle
			if ( highest_angle - current_angle ) > 20:
			
				sendInt(0,car_address)
				time.sleep(2.0)
				print '-------------------------'
				print highest_angle
				print '------------------------'
				action = 0
	
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(img, (9, 9), 0)
		hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
		maskedred = cv2.inRange(hsv, lower_red, upper_red)
		maskedblack = cv2.inRange(hsv, lower_black , upper_black )
		maskedyellow = cv2.inRange(hsv, lower_yellow , upper_yellow )
		maskedgreen = cv2.inRange(hsv,lower_green,upper_green)
		maskedpurple = cv2.inRange(hsv,lower_purple,upper_purple)
		blackcontours, _ = cv2.findContours(maskedblack,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
		redcontours, _ = cv2.findContours(maskedred,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)	
		yellowcontours, _ = cv2.findContours(maskedyellow,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)	
		greencontours, _ = cv2.findContours(maskedgreen,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
		purple_contours , _ = cv2.findContours(maskedpurple , cv2.RETR_TREE , cv2.CHAIN_APPROX_NONE )

		
		if ( len(purple_contours) != 0 and limitdetectpurple == 0 ):

			sendInt(4,car_address)
			time.sleep(0.1)
			sendInt(0,car_address)
			cpurple = max(purple_contours, key = cv2.contourArea)
			purplerect = cv2.minAreaRect(cpurple)	
			purplebox = cv.BoxPoints(purplerect)
			purplebox = np.int0(purplebox)
			purplemidpoint = midpointCalc(purplebox)
			print 'detected'
			if purplemidpoint != None:
				print 'calculated'
				action = 1
				if purplemidpoint[4] > 280 :
					rdir = 2
				elif purplemidpoint[4] < 280:
					rdir = 1

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
				sendInt(4 , car_address)


		if ( limitframe >= limitdelay ):
			lastcolorblack = 0
			noblack = 0
			limitframe = 0
			freeblack = 1
		
		if ( freeblackcount >= 20 ):
			freeblack = 0
			freeblackcount = 0
	elif (action == 1): #block finding
		if rdir == 1 :
			sendInt( 6 , car_address )
		elif rdir == 2 :
			sendInt(5, car_address)
		p.ChangeDutyCycle(6.5)
		distance = calculatedistance()
		if distance < stop_distance:
			action = 2
			time.sleep(0.3)
			sendInt(0,car_address)
	elif (action == 2): #TemplateMatching
		time.sleep(0.5)
		sendInt(0 , car_address )
		time.sleep(0.5)
		print('action2')
		action = readtemplate(img)
		print "next action = " , action 
		if action == 2:
			sendInt(1,car_address)
			time.sleep(0.2)
			sendInt(4,car_address)
			time.sleep(1)
			sendInt(0,car_address)
		elif action == 0 :
			p.ChangeDutyCycle(3.2)
			time.sleep(1)
			action = 8
			limitdetectpurple = 1
			limitdetectpurpleframeval = 30#template matching
			noblack = 0
		elif action == 7: 
			sendInt(6,car_address)
			time.sleep(0.7)
			sendInt(0,car_address)
		elif action == 3:
			limitdetectpurple = 1
			limitdetectpurpleframeval = 30
			p.ChangeDutyCycle(3.2)
			time.sleep(1.5)
	elif ( action == 4 ):
		countshape()
		limitdetectpurple = 1
		limitdetectpurpleframeval = 25
		time.sleep(1)
		action = 8
	elif ( action == 5 ):
		p.ChangeDutyCycle(6.0)
		sendInt(5,car_address)
		action = findball(img)
	elif ( action == 6 ): #readdistance
		print "reading distance..."
		time.sleep(3)
		print 'distance =' , distance
		time.sleep(4)
		p.ChangeDutyCycle(3.2)
		action = 8
		time.sleep(1.5)
		limitdetectpurple = 1
		limitdetectpurpleframeval = 10
	elif ( action == 7 ): #trafficlight
	
		p.ChangeDutyCycle(5.9)
		#print( watchtraffic(img) )
		trafficlightcolor = watchtraffic(img)
		if trafficlightcolor == 'green' :
			sendInt( 5 , car_address )
			action = 8
			p.ChangeDutyCycle(3.2)
			limitdetectpurple = 1
			limitdetectpurpleframe = 15
			time.sleep(1)
	elif ( action == 8 ):
		if rdir == 1:
			sendInt(8,car_address)
		elif rdir == 2:
			sendInt(7,car_address)
		
		if findbackline(img) ==  1:
			action = 0
        elif ( action == 9 ):
		print "check gp"
                action = checkgp(img)
		limitdetectpurple = 1
		limitdetectpurpleval = 60

	if limitdetectpurple == 1 :
		limitdetectpurpleframe += 1

	if limitdetectpurpleframe >= limitdetectpurpleframeval:
		limitdetectpurple = 0
		limitdetectpurpleframe = 0
	
	if showimg == 1 :
		cv2.imshow("color", img)
		
	key = cv2.waitKey(1) & 0xFF

	rawCapture.truncate(0)

	if key==ord('q'):
		sendInt( 0 , car_address )
		GPIO.cleanup();
		break
