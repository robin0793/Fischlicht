#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import logging

log = logging.getLogger("daemon")
errlog = logging.getLogger("error")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)




def setnt(args, pin):
	
	GPIO.setup(pin, GPIO.OUT)
	args[1] = int(args[1])

	if args[1] == 0:
		GPIO.output(pin, GPIO.LOW)
		log.info("Netzteil ausgeschaltet")
	elif args[1] == 1:
		GPIO.output(pin, GPIO.HIGH)
		log.info("Netzteil eingeschaltet")
	else:
		log.warn("Falsches Argument")
