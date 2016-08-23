#!/usr/bin/python3

import smbus
import time

#Shunt Voltage: 0x01
#Bus Voltage: 0x02
#Power Register:  0x03
#Current Register: 0x04
#Calibration Register: 0x05

#I2C-Adresse
address = 0x40

#INIT
print(time.strftime("[%Y-%m-%d %H:%M]"), "[ELEC] Initiere I2C-Verbindung...")

ina219 = smbus.SMBus(1)
mask = 0b11111111

#Config/Calibration Register

ina219.write_i2c_block_data(address,0x00,[0x1F, 0xFF])
ina219.write_i2c_block_data(address,0x05,[0x14, 0xF8])
print(time.strftime("[%Y-%m-%d %H:%M]"), "[ELEC] Konfiguration abgeschlossen")

def shunt():	#Read Shunt Voltage
	v_s = ina219.read_i2c_block_data(address,0x01,2)
	voltage_shunt = (((v_s[0] & mask) << 8) + v_s[1])
	print(time.strftime("[%Y-%m-%d %H:%M]"), "[ELEC] Shunt Spannung:", voltage_shunt/100, "mV")
	return voltage_shunt/100 #mV

def bus():
	v_b = ina219.read_i2c_block_data(address,0x02,2)
	voltage_bus = (((v_b[0] & mask) << 8) + v_b[1])
	print(time.strftime("[%Y-%m-%d %H:%M]"), "[ELEC] Bus Spannung:", round(voltage_bus/2000, 2), "V")
	return round(voltage_bus/2000, 2) #V

def power():
	po = ina219.read_i2c_block_data(address,0x03,2)
	power = (((po[0] & mask) << 8) + po[1])
	print(time.strftime("[%Y-%m-%d %H:%M]"), "[ELEC] Leistungsaufnahme:", power/50, "W")
	return power/50 #W
	
def current():
	cu = ina219.read_i2c_block_data(address,0x04,2)
	current = (((cu[0] & mask) << 8) + cu[1])
	print(time.strftime("[%Y-%m-%d %H:%M]"), "[ELEC] Stromaufnahme:", current/1000, "A")
	return current/1000 #A

if __name__ == "__main__":
	print("Shunt:  ", shunt(), " mV")
	print("Bus:    ", bus(), " mV")
	print("Power:  ", power(), "W")
	print("Current:", current(), "A")


