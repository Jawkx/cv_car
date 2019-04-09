import picamera
from time import sleep
camera = picamera.PiCamera()
camera.resolution = (560,256)

name = input('name:')
camera.capture(name)
