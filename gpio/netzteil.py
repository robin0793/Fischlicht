#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)




def setnt(args, pin):
	
	GPIO.setup(pin, GPIO.OUT)
	args[1] = int(args[1])

	if args[1] == 0:
		GPIO.output(pin, GPIO.LOW)
		print(time.strftime("[%Y-%m-%d %H:%M]"), "[ NT ] Netzteil ausgeschaltet")
	elif args[1] == 1:
		GPIO.output(pin, GPIO.HIGH)
		print(time.strftime("[%Y-%m-%d %H:%M]"), "[ NT ] Netzteil eingeschaltet")
	else:
		print(time.strftime("[%Y-%m-%d %H:%M]"), "[ NT ] Falsches Argument")
