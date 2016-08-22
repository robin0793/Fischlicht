#!/usr/bin/python3

import smbus
import time


# I2C-Adresse des A/D-Wandlers
address = 0x4f

# Erzeugen einer I2C-Instanz und Offnen des Busses
adw = smbus.SMBus(1)

while True:
	a_0 = adw.read_i2c_block_data(address, 0x40)


	print (a_0)
	time.sleep (0.5)
	