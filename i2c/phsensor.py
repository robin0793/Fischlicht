#!/usr/bin/python3

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

#Berechnung
def calc_ph(value,pH4,pH7):
	try:
		m = (7.00 - 4.00) / (pH7 - pH4)
		n = 7.00 - m * pH7
		
		pH = m * value + n
		
		return(pH)
	except:
		return(0)
		
#Calibration Values
PH4 = 2265
PH7 = 2052

def read(PH4, PH7, volts = 0):
	voltage = []

	for k in range(0,1000):
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
	log.info("Gemessener PH-Wert: {}".format(phwert))
	return phwert

if __name__ == "__main__":
	phwert = read(PH4,PH7,1)
	print ("pH-Wert: {}".format(phwert))	
	if phwert >= 7.3:
		os.system("/home/pi/raspberry-remote/send 10111 3 1")
	elif phwert <=7.25:
		os.system("/home/pi/raspberry-remote/send 10111 3 0")
