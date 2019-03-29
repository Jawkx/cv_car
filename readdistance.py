import cv2
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


trigger = 21 #tbd
echo = 20  #tbd

GPIO.setup(trigger,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)

#GPIO.cleanup()
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


while True :
    print('distance',calculatedistance())
    time.sleep(0.01)
