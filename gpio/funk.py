import os
import time
import RPi.GPIO as GPIO
import logging

log = logging.getLogger("daemon")
errlog = logging.getLogger("error")

GPIO.setwarnings(False)

code = [1,0,1,1,1]
pin = 17

#"elropi.py" for switching Elro devices using Python on Raspberry Pi
#by Heiko H. 2012
 
class RemoteSwitch(object):
        repeat = 10 # Number of transmissions
        pulselength = 300 # microseconds
        GPIOMode = GPIO.BCM
       
        def __init__(self, device, key=[1,1,1,1,1], pin=4):
                '''
                devices: A = 1, B = 2, C = 4, D = 8, E = 16  
                key: according to dipswitches on your Elro receivers
                pin: according to Broadcom pin naming
                '''            
                self.pin = pin
                self.key = key
                self.device = device
                GPIO.setmode(self.GPIOMode)
                GPIO.setup(self.pin, GPIO.OUT)
               
        def switchOn(self):
                self._switch(GPIO.HIGH)
 
        def switchOff(self):
                self._switch(GPIO.LOW)
 
        def _switch(self, switch):
                self.bit = [142, 142, 142, 142, 142, 142, 142, 142, 142, 142, 142, 136, 128, 0, 0, 0]          
 
                for t in range(5):
                        if self.key[t]:
                                self.bit[t]=136
                x=1
                for i in range(1,6):
                        if self.device & x > 0:
                                self.bit[4+i] = 136
                        x = x<<1
 
                if switch == GPIO.HIGH:
                        self.bit[10] = 136
                        self.bit[11] = 142
                               
                bangs = []
                for y in range(16):
                        x = 128
                        for i in range(1,9):
                                b = (self.bit[y] & x > 0) and GPIO.HIGH or GPIO.LOW
                                bangs.append(b)
                                x = x>>1
                               
                GPIO.output(self.pin, GPIO.LOW)
                for z in range(self.repeat):
                        for b in bangs:
                                GPIO.output(self.pin, b)
                                time.sleep(self.pulselength/1000000.)

def send(pin, code, status):

	log.info("Switch {}: {}".format(pin, status))
	remote = RemoteSwitch(pin, code, pin)
	if status == 1:
		remote.switchOn()
	elif status == 0:
		remote.switchOff()


							
              
				


				

