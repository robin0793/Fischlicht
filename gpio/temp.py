import time
import logging

log = logging.getLogger("daemon")
errlog = logging.getLogger("error")

def read(deviceid, name):

	
	try:
		fileobj = open("/sys/bus/w1/devices/"+deviceid+"/w1_slave",'r')
		
		lines = fileobj.readlines()
		fileobj.close()
	except:
		error = 1
		return 0

	# get the status from the end of line 1 
	status = lines[0][-4:-1]

	# is the status is ok, get the temperature from line 2
	if status=="YES":
		tempstr= lines[1][-6:-1]
		tempvalue=float(tempstr)/1000
		log.info("{}: {}°C".format(name.upper(),round(tempvalue,1)))
		return round(tempvalue,1)
	else:
		log.info("Fehler beim Lesen des Sensors: {}".format(name))
		error = 1
		return 0