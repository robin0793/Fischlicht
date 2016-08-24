import RPi.GPIO as GPIO

import sys
import time
from os import path

GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
 #set pin 18 to output
path = path.dirname(path.realpath(__file__))

def setfan(args, pin):

	GPIO.setup(pin, GPIO.OUT)

	if int(args[1]) == 0:
		GPIO.output(pin, GPIO.LOW)
		print(time.strftime("[%Y-%m-%d %H:%M]"), "[FAN ] Lüfter ausgeschaltet")
	elif int(args[1]) == 1:
		GPIO.output(pin, GPIO.HIGH)
		print(time.strftime("[%Y-%m-%d %H:%M]"), "[FAN ] Lüfter eingeschaltet")
	else:
		print(time.strftime("[%Y-%m-%d %H:%M]"), "[FAN ] Falsches Argument")
	
	
	#status = int(arg_array[1])
	#print(time.strftime("[%Y-%m-%d %H:%M]"), "[FAN ] Setze Lüfter auf", status, "%")
	#if status != 0: status = status/5+80

	#p = GPIO.PWM(pin, 25)        #set the PWM on pin 21 to 25Hz
	#p.start(0) # Starte das PWM
	#print (int(status))
	#p.ChangeDutyCycle(int(status))

		
if __name__ == "__main__":
	from sys import argv
	setfan(argv,18)
