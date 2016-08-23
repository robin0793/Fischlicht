#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
GPIO.setup(22, GPIO.OUT)



def setnt(args):
	args[1] = int(args[1])

	if args[1] == 0:
		GPIO.output(22, GPIO.LOW)
		print(time.strftime("[%Y-%m-%d %H:%M]"), "[ NT ] Netzteil ausgeschaltet")
	elif args[1] == 1:
		GPIO.output(22, GPIO.HIGH)
		print(time.strftime("[%Y-%m-%d %H:%M]"), "[ NT ] Netzteil eingeschaltet")
	else:
		print(time.strftime("[%Y-%m-%d %H:%M]"), "[ NT ] Falsches Argument")
