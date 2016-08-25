import time

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
		print(time.strftime("[%Y-%m-%d %H:%M]"), "[TEMP]", name, ":", round(tempvalue,1))
		return round(tempvalue,1)
	else:
		print(time.strftime("[%Y-%m-%d %H:%M]"), "[TEMP] Fehler beim Lesen des Sensors:", name)
		error = 1
		return 0