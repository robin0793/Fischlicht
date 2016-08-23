import time

def read(sensor):

	dict = {"1" : "28-000005986837",
			"2" : "28-000005985d20",
			"r" : "28-000005af42fe",
			"c" : "10-000802e4371a"}
			
	deviceid = dict[sensor]
	
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
		print(time.strftime("[%Y-%m-%d %H:%M]"), "[TEMP]", sensor, ":", round(tempvalue,1))
		return round(tempvalue,1)
	else:
		print(time.strftime("[%Y-%m-%d %H:%M]"), "[TEMP] Fehler beim Lesen des Sensors:", sensor)
		error = 1
		return 0