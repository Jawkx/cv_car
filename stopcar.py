import smbus
import RPi.GPIO as GPIO

bus = smbus.SMBus(1)
car_address = 0x04

def sendInt(value,address):
	bus.write_byte(address, value)

    	return -1

sendInt(1,car_address)