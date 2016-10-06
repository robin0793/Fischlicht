import os
import time
import RPi.GPIO as GPIO
import logging

log = logging.getLogger("daemon")
errlog = logging.getLogger("error")




class flow():

	def rise_detected(self, alert):
		self.counter += 1

	def __init__(self, pin):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		self.pin = pin
		GPIO.setup(self.pin, GPIO.IN)
		GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.rise_detected)
		
		self.counter = 0
		self.flow = 0
		
	def read(self, stime=1):
		self.counter=0
		time.sleep(stime)
		
		self.pulses = self.counter
		
		self.flowrate = round((self.pulses * (60/stime)) / 5.5)
		log.info("Flow Rate: {} l/h".format(self.flowrate))
		
	
	
if __name__ == "__main__":
	
	flow = flow(pin = 5)
	
	#time.sleep(5)
	flow.read(1)
	print("Pulses: {}".format(flow.pulses))
	print("Flow: {} l/h".format(flow.flowrate))
