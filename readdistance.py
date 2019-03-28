import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

trigger = 18 #tbd
echo = 24  #tbd


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
    distance = (TimeElapsed * 34300) / 2
 
    return distance

while True :
    print(calculatedistance)
    time.sleep(0.1)