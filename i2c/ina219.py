#!/usr/bin/python3
try:
	import smbus
	import time
	import logging

	log = logging.getLogger("daemon")
	errlog = logging.getLogger("error")

	#Shunt Voltage: 0x01
	#Bus Voltage: 0x02
	#Power Register:  0x03
	#Current Register: 0x04
	#Calibration Register: 0x05

	#I2C-Adresse
	address = 0x40

	#INIT
	log.info("Initiere I2C-Verbindung...")

	ina219 = smbus.SMBus(1)
	mask = 0b11111111

	#Config/Calibration Register

	ina219.write_i2c_block_data(address,0x00,[0x1F, 0xFF])
	ina219.write_i2c_block_data(address,0x05,[0x14, 0xF8])
	log.info("Konfiguration abgeschlossen")
except Exception as E:
	log.warn("Fehler beim Herstellen der i2c-Verbindung. \'smbus\'-Modul installiert?")
	
	
def shunt():	#Read Shunt Voltage
	v_s = ina219.read_i2c_block_data(address,0x01,2)
	voltage_shunt = (((v_s[0] & mask) << 8) + v_s[1])
	log.info("Shunt Spannung: {} mV".format(voltage_shunt/100))
	return voltage_shunt/100 #mV

def bus():
	v_b = ina219.read_i2c_block_data(address,0x02,2)
	voltage_bus = (((v_b[0] & mask) << 8) + v_b[1])
	log.info("Bus Spannung: {} V".format(round(voltage_bus/2000, 2)))
	return round(voltage_bus/2000, 2) #V

def power():
	po = ina219.read_i2c_block_data(address,0x03,2)
	power = (((po[0] & mask) << 8) + po[1])
	log.info("Leistungsaufnahme: {} W".format(power/50))
	return power/50 #W
	
def current():
	cu = ina219.read_i2c_block_data(address,0x04,2)
	current = (((cu[0] & mask) << 8) + cu[1])
	log.info("Stromaufnahme: {} A".format(current/1000))
	return current/1000 #A

if __name__ == "__main__":
	print("Shunt:  ", shunt(), " mV")
	print("Bus:    ", bus(), " mV")
	print("Power:  ", power(), "W")
	print("Current:", current(), "A")


