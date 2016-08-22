import RPi.GPIO as GPIO  
import sys
from os import path

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT) #set pin 18 to output

path = path.dirname(path.realpath(__file__))

if len(sys.argv) > 1:
	status=int(sys.argv[1])
	if status != 0: status/5+80
else:
	f = open(path+"/luefter.txt","r")
	status=f.read()
	f.close()

p = GPIO.PWM(18, 25)        #set the PWM on pin 21 to 25Hz
p.start(0) # Starte das PWM
print (int(status))
p.ChangeDutyCycle(int(status))

f = open(path+"/luefter.txt","w")
f.write(str(status))
f.close()
