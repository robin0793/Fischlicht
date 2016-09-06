#!/usr/bin/python3
try:
	import smbus
	import time
	import os
	import logging

	log = logging.getLogger("daemon")
	errlog = logging.getLogger("error")
	#PH Wert: 0x00

	#I2C-Adresse 
	address = 0x48

	#INIT
	log.info("Initiere I2C-Verbindung...")
	ph = smbus.SMBus(1)




except Exception as E:
	log.warn("Fehler beim Herstellen der i2c-Verbindung. \'smbus\'-Modul installiert?")

#Berechnung
def calc_ph(value,pH4,pH7):
	try:
		m = (7.00 - 4.00) / (pH7 - pH4)
		n = 7.00 - m * pH7
		
		pH = m * value + n
		
		return(pH)
	except:
		return(0)
	

def read(PH4 = 0, PH7 = 0, volts = 0):
	voltage = []

	for k in range(0,500):
		reading = ph.read_i2c_block_data(address, 0x00)
		for j in range (0,1):
			p1 = reading[j*2]
			p2 = reading[j*2+1]
			voltage.append ((p1 << 8) + p2)

	voltage_avg = sum(voltage) / len(voltage)

	if volts == 1: 
		log.info(voltage_avg)
		return voltage_avg

	phwert = round(calc_ph(voltage_avg, PH4, PH7),2)
	if __name__ != "__main__": log.info("Gemessener PH-Wert: {}".format(phwert))
	return phwert
	
def calib(v):
	input("Messung PH{} (Enter druecken, wenn bereit).".format(v))
	print ("10 Erfolgreiche Messungen (Toleranz +- 1 mV). Abbruch mit CTRL+C")
	print()
	counter = 0
	cal_ph_cmp = 0
	try:
		while counter < 10:
			cal_ph = round(read(volts=1),1)
			if abs(cal_ph - cal_ph_cmp) < 1:
				counter += 1
			else:
				counter = 0
				cal_ph_cmp = cal_ph
			print("Messung PH{}: {} mV [{}]".format(v, cal_ph, counter))	
			time.sleep(2)
		print()
		print ("Ergebnis der Messung für PH{}: {} mV".format(v, cal_ph_cmp))	
		print()
		return cal_ph_cmp
	except KeyboardInterrupt:
		print ("Messung abgebrochen")
		return	0

if __name__ == "__main__":
	from sys import argv
	if len(argv) > 1 and argv[1] == "calibrate":
		cal_ph7 = calib("7")
		cal_ph4 = calib("4")
		if len(argv) > 2 and os.path.isfile(argv[2]) == True:
			pipe = argv[2]
			print ("Werte an Daemon weitergeben ({})".format(pipe))
			os.system("echo phcal {} {} > {}".format(cal_ph7, cal_ph4, pipe))