#!/usr/bin/python3

import sys, time, os
from _thread import start_new_thread as thread
from os import path
import configparser
import logging
import traceback


__version__ = "2.1"

#Logging
def setup_log(name, file, wmode, std):
	format = logging.Formatter(fmt="[%(asctime)s][%(levelname).4s][%(module)-4.4s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
	handler = logging.FileHandler(file, mode=wmode)
	handler.setFormatter(format)
	stream = logging.StreamHandler(std)
	stream.setFormatter(format)
	log = logging.getLogger(name)

	log.setLevel(logging.DEBUG)
	log.addHandler(handler)
	log.addHandler(stream)
	return log

log = setup_log("daemon", "/var/log/Fischlicht/daemon.log", "w", sys.stdout)
errlog = setup_log("error", "/var/log/Fischlicht/error.log", "a", sys.stderr)

try:
	import telepot
except Exception as e:
	log.warn("Telepot Modul konnte nicht importiert werden. Telegram Bot nicht verfügbar!")

import i2c.phsensor as ph
import i2c.ina219 as ina

import database.db as db
import gpio.temp as temp
import gpio.funk as funk
import gpio.luefter as fan
import gpio.flow as flow
import gpio.netzteil as nt
import spi.led as led

#import i2c.pcf8591 as ad

path = path.dirname(path.realpath(__file__))

#Exit Funktion
def exiting():
	log.info("Fischlicht wird beendet")
	db.write_setting("lichtprogramm", licht.intens, 1)
	db.write_setting("lichtprogramm", licht.aktiv)
	db.close()
	logging.shutdown()
	quit()


print()
log.info("Willkommen!")
log.info("Fischlicht {}".format(__version__))
print()
log.info("Config einlesen")

config = configparser.ConfigParser()
config.read("{}/config.ini".format(path))

outlet_code = list(map(int, config["outlet"]["code"].split(",")))
led_assign = list(map(int, config["led"]["assign"].split(",")))

try:
	led_intens = list(map(float, db.read_setting("lichtprogramm").split(";")))
	led_aktiv = db.read_setting("lichtprogramm", "text")
except:
	led_intens = [0]
	led_aktiv = "off"
	
licht = led.led(zuordnung=led_assign, intens = led_intens, aktiv = led_aktiv)

remote_ph = funk.RemoteSwitch(int(config["ph"]["outlet"]), outlet_code, int(config["outlet"]["pin"]))

if config["power"]["mode"] == "outlet":
	remote_nt = funk.RemoteSwitch(int(config["power"]["pin"]), outlet_code, int(config["outlet"]["pin"]))


if "flow" in config and int(config["flow"]["active"]) == 1: 
	flow = flow.flow(pin = int(config["flow"]["pin"]))

def alert(nachricht, wert, einheit="", userid=""):
	try:
		log.warn("{}: {} {}".format(nachricht, wert, einheit))
		if userid != "": bot.sendMessage(userid, "{}: {} {}".format(nachricht, wert, einheit))
	except:
		log.error("Telegram Bot: Fehler beim senden")

def bot_handle(msg):
	log.info("[TBOT] Nachricht empfangen: {}".format(msg))

if int(config["telebot"]["active"]) == 1:	
	log.info("Telegram Bot einrichten")
	
	bot = telepot.Bot(config["telebot"]["bot_id"]) #BOT ID hier einfügen
	userid = config["telebot"]["user_id"] #User ID hier einfügen
	
	bot.message_loop(bot_handle)
else: userid = ""


def listen(): #Auf Eingaben reagieren indem die Datei "pipe" ausgelesen wird
	log.info("Bereit fuer Eingaben.")
	open(path + "/pipe", "w").close() # 
	p = open(path + "/pipe", "r")
	while True:
		
		eingabe = p.read()
		if eingabe != "": #Eingabe vorhanden
			log.info("Eingabe erkannt: {}".format(eingabe))
			try:
				args = eingabe.split()
				if args[0] == "led": # led [lichtprogramm] [dauer]
					thread(licht.setled,(args, )) #Neuer Thread zum Aendern des Lichts
					
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
						remote_nt.switchOn()
						
					db.write_setting("netzteil", args[1])
				elif args[0] == "phcal":
					if len(args)>2:
						if float(args[1]) != 0: db.write_setting("ph7", float(args[1]))
						if float(args[2]) != 0: db.write_setting("ph4", float(args[2]))
					else: 
						log.warn("phcal: Zu wenig Argumente")
				elif args[0] == "cleardb": #alte DB Eintraege löschen (>7Tage)
					db.delete_old()
				elif args[0] == "stop": 
					exiting()
			except Exception as e :
				log.info("Ungültige Eingabe?")
				errlog.error(e)	
				
			p.close()
			open(path + "/pipe", "w").close()
			p = open(path + "/pipe", "r")
			
		time.sleep(0.5)

	p.close()

thread(listen,()) #Thread starten

try:
#LOOP
	log.info("Starte Daemon.")
	if int(config["ph"]["active"]) == 1: 
		if db.read_setting("co2") == None: db.write_setting("co2", 0)
		phwert = db.read_last("ph")
	
	if config["power"]["mode"] == "gpio":
		nt.setnt(["nt", db.read_setting("netzteil")], int(config["power"]["pin"]))
	elif config["power"]["mode"] == "outlet":
		remote_nt.switch(int(db.read_setting("netzteil")))
	

	
	thread(licht.setled,(["led", licht.aktiv, 1, 1], ))
	
	fanstatus = 0
	sent = 0
	
	while True:
	
		db_array = []
		
	#PHWERT
		if int(config["ph"]["active"]) == 1:
			
			ph4 = db.read_setting("ph4")
			ph7 = db.read_setting("ph7")
			phstatus = db.read_setting("co2")
			phwert_prev = phwert
			phwert = ph.read(ph4,ph7)
			
			db_array = db.add_write(db_array, "ph", phwert)

			if phwert_prev == None: phwert_prev = phwert
			
			for n in range(0,5):
				if abs(phwert - phwert_prev) < 0.2: break
				phwert = ph.read(ph4,ph7)
				
			if abs(phwert - phwert_prev) < 0.2:
				phwert = phwert_prev
			
			if phwert >= float(config["ph"]["ph_value"]) and phstatus == 0:
				if db.read_setting("netzteil") == 1:
					remote_ph.switchOn()
					db.write_setting("co2", 1)
			elif phwert <= float(config["ph"]["ph_value"]) - 0.05 and phstatus == 1:
				remote_ph.switchOff()
				db.write_setting("co2", 0)
		
	#TEMP
		if int(config["temp"]["active"]) == 1:
			temp_sensors = config.options("temp")
			try: 
				temp_array 
			except NameError:
				temp_array = []
				for g in range(0, len(temp_sensors)):
					temp_array.append([0, 0, 0])

			for g in range(1, len(temp_sensors)):

				if os.path.isfile("/sys/bus/w1/devices/{}/w1_slave".format(temp_sensors[g])) == True:
					
					sensor_array = config["temp"][temp_sensors[g]].split(",")
					temp_array[g][0] = temp.read(temp_sensors[g], sensor_array[0])
					
					db_array = db.add_write(db_array, "temp_{}".format(sensor_array[0]), temp_array[g][0])
					
					#low_alert
					if len(sensor_array) > 3 and temp_array[g][0] < float(sensor_array[3]) and temp_array[g][2] == 0: 
						if sensor_array[0] == "case":
							fan.setfan(["fan", 0], int(config["fan"]["pin"]))
							fanstatus = 0
						else:
							alert("Temperatur {} kritisch niedrig".format(sensor_array[0]), temp_array[g][0], "°C", userid)
							temp_array[g][2] = 1
					#low_warning		
					elif len(sensor_array) > 1 and temp_array[g][0] < float(sensor_array[1]) and temp_array[g][1] == 0 and sensor_array[0] != "case": 
						alert("Temperatur {} zu niedrig".format(sensor_array[0]), temp_array[g][0], "°C", userid)
						temp_array[g][1] = 1
					if temp_array[g][0] > float(sensor_array[1]) and sensor_array[0] == "case":
						fan.setfan(["fan", 1], int(config["fan"]["pin"]))
						fanstatus = 1
					
					#high_alert		
					if len(sensor_array) > 4 and temp_array[g][0] > float(sensor_array[4]) and temp_array[g][2] == 0: 
						alert("Temperatur {} kritisch hoch".format(sensor_array[0]), temp_array[g][0], "°C", userid)
						temp_array[g][2] = 1
					
					#high_warning	
					elif len(sensor_array) > 2 and temp_array[g][0] > float(sensor_array[2]) and temp_array[g][1] == 0: 

						alert("Temperatur {} zu hoch".format(sensor_array[0]), temp_array[g][0], "°C", userid)
						temp_array[g][1] = 1
							
					# Zurücksetzen, falls Temperatur wieder ok (+- 0.2 Grad)
					if len(sensor_array) > 2 and float(sensor_array[1])+0.2 < temp_array[g][0] < float(sensor_array[2])-0.2: #gruener Bereich
						temp_array[g][1] = 0 #Warning aus
						temp_array[g][2] = 0 #Alarm aus
					elif len(sensor_array) > 4 and float(sensor_array[3])+0.2 < temp_array[g][0] < float(sensor_array[4])-0.2: #Warnung Bereich
						temp_array[g][2] = 0 #Alarm aus

		
	#ELECTRIC 
		if int(config["ina219"]["active"]) == 1:
			volt = ina.bus()
			if volt <= 0.2:
				volt = 0
				current = 0
			else:
				current = ina.current()
			
			db_array = db.add_write(db_array, "volt", volt)
			db_array = db.add_write(db_array, "current", current)
	
	#FLOW
		if "flow" in config and int(config["flow"]["active"]) == 1:
			flow.read(stime=5)
			db_array = db.add_write(db_array, "flow", flow.flowrate)
		
		#f= open(path + "/phvolt.csv","a")
		#f.write("{};{}\n".format(str(phwert).replace(".",","),str(volt).replace(".",",")))
		#f.close()		
			
	#WRITE TO DATABASE
		db.write_all(db_array)
			
		print()
		time.sleep(int(config["general"]["interval"]))
		
except KeyboardInterrupt:
	log.info("Abbruch durch KeyboardInterrupt")

		
except Exception as e:
	errlog.error("Abbruch: {}".format(e))
	errlog.error(traceback.format_exc())




	
