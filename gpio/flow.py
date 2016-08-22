import os
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pin_flow = 5
GPIO.setup(pin_flow, GPIO.IN) #set pin 18 to output

def alert(channel):
	print("GPIO {} HIGH".format(channel))
	
def alert_reset(channel):
	print("GPIO LOW")

GPIO.add_event_detect(pin_flow, GPIO.RISING, callback=alert)

while True:
	time.sleep(0.1)