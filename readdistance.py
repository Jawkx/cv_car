import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


trigger = 24 #tbd
echo = 18  #tbd

GPIO.setup(trigger,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)

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
    print(calculatedistance())
    time.sleep(0.1)