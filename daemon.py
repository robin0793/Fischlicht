#!/usr/bin/python3

import sys, time, os
from _thread import start_new_thread as thread
from os import path
import telepot
import configparser

__version__ = "2.0"

import i2c.phsensor as ph
import i2c.ina219 as ina
import database.db as db
import gpio.temp as temp
import gpio.funk as funk
import gpio.luefter as fan
import gpio.netzteil as nt
import spi.led as led

#import i2c.pcf8591 as ad

path = path.dirname(path.realpath(__file__))



print()
print(time.strftime("[%Y-%m-%d %H:%M]"), "[MAIN] Willkommen!")
print(time.strftime("[%Y-%m-%d %H:%M]"), "[MAIN] Fischlicht", __version__)
print()
print(time.strftime("[%Y-%m-%d %H:%M]"), "[MAIN] Config einlesen")

config = configparser.ConfigParser()
config.read("{}/config.ini".format(path))

outlet_code = list(map(int, config["outlet"]["code"].split(",")))

def alert(nachricht, wert, einheit="", userid=""):
	print(time.strftime("[%Y-%m-%d %H:%M]"), "[ALRT] {}: {} {}".format(nachricht, wert, einheit))
	if userid != "": bot.sendMessage(userid, "{}: {} {}".format(nachricht, wert, einheit))

def bot_handle(msg):
	print(time.strftime("[%Y-%m-%d %H:%M]"), "[TBOT] Nachricht empfangen:", msg)

if int(config["telebot"]["active"]) == 1:	
	print(time.strftime("[%Y-%m-%d %H:%M]"), "[MAIN] Telegram Bot einrichten")
	
	bot = telepot.Bot(config["telebot"]["bot_id"]) #BOT ID hier einfügen
	userid = config["telebot"]["user_id"] #User ID hier einfügen
	
	bot.message_loop(bot_handle)
else: userid = ""


def listen(): #Auf Eingaben reagieren indem die Datei "pipe" ausgelesen wird
	print(time.strftime("[%Y-%m-%d %H:%M]"), "[MAIN] Bereit fuer Eingaben.")
	open(path + "/pipe", "w").close() # 
	p = open(path + "/pipe", "r")
	while True:
		
		eingabe = p.read()
		if eingabe != "": #Eingabe vorhanden
			print(time.strftime("[%Y-%m-%d %H:%M]"), "[MAIN] Eingabe erkannt:", eingabe)
			try:
				args = eingabe.split()
				if args[0] == "led": # led [lichtprogramm] [dauer]
					thread(led.setled,(args,)) #Neuer Thread zum Aendern des Lichts
					db.write_setting("lichtprogramm", args[1]) #Lichtprogramm in Datenbank schreiben
					
				elif args[0] == "fan":
					if len(args) < 2: 
						fanspeed=db.read_setting("luefter")
						args.append(fanspeed)
					fan.setfan(args, int(config["fan"]["pin"]))
					db.write_setting("luefter", args[1])
					
				elif args[0] == "nt":
					if len(args) < 2: 
						ntstatus=db.read_setting("netzteil")
						args.append(ntstatus)
						
					if config["power"]["mode"] == "gpio":
						nt.setnt(args, int(config["power"]["pin"]))
					elif config["power"]["mode"] == "outlet":
						funk.send(int(config["power"]["pin"]), outlet_code, 1)
						
					db.write_setting("netzteil", args[1])
					
				elif args[0] == "cleardb": #alte DB Eintraege löschen (>7Tage)
					db.delete_old()
			except Exception as e :
				print(time.strftime("[%Y-%m-%d %H:%M]"), "[MAIN] Ungültige Eingabe?")
				print(time.strftime("[%Y-%m-%d %H:%M]"), "[MAIN][ERROR]" , e)	
				
			p.close()
			open(path + "/pipe", "w").close()
			p = open(path + "/pipe", "r")
			
		time.sleep(0.5)

	p.close()

thread(listen,()) #Thread starten

try:
#LOOP
	print(time.strftime("[%Y-%m-%d %H:%M]"), "[MAIN] Starte Daemon.")
	if int(config["ph"]["active"]) == 1: phwert = db.read_last("ph")

	
	if config["power"]["mode"] == "gpio":
		nt.setnt(["nt", db.read_setting("netzteil")], int(config["power"]["pin"]))
	elif config["power"]["mode"] == "outlet":
		funk.send(int(config["power"]["pin"]), outlet_code, db.read_setting("netzteil"))
	

	
	thread(led.setled,(["led", db.read_setting("lichtprogramm", "text"), 1],))
	
	fanstatus = 0
	sent = 0
	
	while True:
	
	#PHWERT
		if int(config["ph"]["active"]) == 1:
			ph4 = db.read_setting("ph4")
			ph7 = db.read_setting("ph7")
			phstatus = db.read_setting("co2")
			phwert_prev = phwert
			phwert = ph.read(ph4,ph7)
			
			
			for n in range(0,5):
				if abs(phwert - phwert_prev) < 0.2: break
			if phwert >= float(config["ph"]["ph_value"]) and phstatus == 0:
				if db.read_setting("netzteil") == 1:
					funk.send (int (config["ph"]["outlet"]), outlet_code, 1)
					db.write_setting("co2", 1)
			elif phwert <= float(config["ph"]["ph_value"]) - 0.5 and phstatus == 1:
				funk.send (int (config["ph"]["outlet"]), outlet_code, 0)
				db.write_setting("co2", 0)
			
		
	#TEMP
		if int(config["temp"]["active"]) == 1:
			temp_sensors = config.options("temp")
			temp_array = [[0,0,0]] * len(temp_sensors)
			
			for g in range(1, len(temp_sensors)):
				
				if os.path.isfile("/sys/bus/w1/devices/{}/w1_slave".format(temp_sensors[g])) == True:
					sensor_array = config["temp"][temp_sensors[g]].split(",")
					temp_array[g][0] = temp.read(temp_sensors[g], sensor_array[0])

					if len (sensor_array) > 3 and temp_array[g][0] < float(sensor_array[3]) and temp_array[g][2] == 0: 
						alert("Temperatur {} kritisch niedrig".format(sensor_array[0]), temperature, "°C", userid)
						temp_array[g][2] = 1
					elif temp_array[g][0] < float(sensor_array[1]) and temp_array[g][2] == 0: 
						if sensor_array[0] == "case":
							fan.setfan(["fan", 0], int(config["fan"]["pin"]))
							fanstatus = 0
						else:
							alert("Temperatur {} zu niedring".format(sensor_array[0]), temperature, "°C", userid)
							temp_array[g][1] = 1
						
					if len (sensor_array) > 4 and temp_array[g][0] > float(sensor_array[4]) and temp_array[g][2] == 0: 
						if sensor_array[0] == "case":
							fan.setfan(["fan", 0], int(config["fan"]["pin"]))
							fanstatus = 0
						#kein else!
						alert("Temperatur {} kritisch hoch".format(sensor_array[0]), temperature, "°C", userid)
						temp_array[g][2] = 1
					elif temp_array[g][0] > float(sensor_array[2]) and temp_array[g][2] == 0: 
						if sensor_array[0] == "case":
							fan.setfan(["fan", 0], int(config["fan"]["pin"]))
							fanstatus = 0
						else:
							alert("Temperatur {} zu hoch".format(sensor_array[0]), temperature, "°C", userid)
							temp_array[g][1] = 1
							
					# Zurücksetzen, falls Temperatur wieder ok (+- 0.2 Grad)
					if float(sensor_array[1])+0.2 < temp_array[g][0] < float(sensor_array[2])-0.2: #gruener Bereich
						temp_array[g][1] = 0 #Warning aus
						temp_array[g][2] = 0 #Alarm aus
					elif float(sensor_array[3])+0.2 < temp_array[g][0] < float(sensor_array[4])-0.2: #Warnung Bereich
						temp_array[g][2] = 0 #Alarm aus

		
		
	#ELECTRIC 
		if int(config["ina219"]["active"]) == 1:
			volt = ina.bus()
			if volt <= 0.2:
				volt = 0
				current = 0
			else:
				current = ina.current()
			
			
		#f= open(path + "/phvolt.csv","a")
		#f.write("{};{}\n".format(str(phwert).replace(".",","),str(volt).replace(".",",")))
		#f.close()		
			
	#WRITE TO DATABASE
		#db.write_all(temp_1 = temp_1, temp_2 = temp_2, temp_r = temp_r, temp_c = temp_c, ph = phwert, volt = volt, current = current)
			
		print()
		time.sleep(int(config["general"]["interval"]))
		
except KeyboardInterrupt:
	print(time.strftime("[%Y-%m-%d %H:%M]"), "[MAIN] Abbruch durch KeyboardInterrupt")
	db.close()
