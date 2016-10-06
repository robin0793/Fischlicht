#!/usr/bin/python3

import os
import sys

if not os.geteuid() == 0:
	print("Run as root!")
	exit()
	
path = os.path.dirname(os.path.realpath(__file__))
print ("Scriptpfad: {}\n".format(path))
try:
	print ("Erstelle Verknüfung in /usr/bin ...")
	inputpy = """#!/usr/bin/python3

import sys
import os
from time import sleep

if len(sys.argv)>1:
	
	allarguments = sys.argv[1] 
	for e in range(2,len(sys.argv)):
		allarguments = "{{}} {{}}".format(allarguments, sys.argv[e]) 


	if sys.argv[1]=="ledm":
		print ("Coming soon... ;)")
		
	elif sys.argv[1]=="log":
		linenr = int(sys.argv[2]) if len(sys.argv)>2 else 10			
		print("/var/log/Fischlicht/daemon.log")
		sleep(1)
		os.system("tail -n{{}} /var/log/Fischlicht/daemon.log".format(linenr))
		
	elif sys.argv[1]=="errlog":
		linenr = int(sys.argv[2]) if len(sys.argv)>2 else 10			
		print("/var/log/Fischlicht/error.log")
		sleep(1)
		os.system("tail -n{{}} /var/log/Fischlicht/error.log".format(linenr))
		
	elif sys.argv[1]=="daemon":
		if not os.geteuid() == 0:
			print("Run as root!")
			exit()
		os.system("systemctl restart fischlicht")
		
	elif sys.argv[1]=="phcal":
		os.system("{path}/i2c/phsensor.py calibrate {path}/pipe")

		
	else:
		os.system("echo {{}} > {path}/pipe".format(allarguments))
		if sys.argv[1]=="led": 
			sleep(2)
			os.system("grep \\\"\[led \]\\\" /var/log/Fischlicht/daemon.log | tail -n5")
		else:
			sleep(1)
			os.system("tail -n1 /var/log/Fischlicht/daemon.log")
else:
	print(\"\"\"\
                            o   __//_
 ┌─┐┬┌─┐┌─┐┬ ┬┬  ┬┌─┐┬ ┬┌┬┐  ° / o   \/|
 ├┤ │└─┐│  ├─┤│  ││  ├─┤ │     >   C==||
 └  ┴└─┘└─┘┴ ┴┴─┘┴└─┘┴ ┴ ┴     \\_____/\\|
                                  \\\\\\\\\\\\

Usage: aq <command> [<args>]

Commands:
  led     [lichtprogramm] [dauer]  Aendern des Lichtprogrammes
  nt      [0|1]                    Netzteil schalten
  fan     [0-100]                  Lüfterdrehzahl setzen [%]
  phcal                            PH-Elektrode kalibrieren
  cleardb                          Alte Datenbankeintraege loeschen (>7 Tage)
  
  log     <[# of lines]>           Letzte Ausgabe des Daemons
  errlog  <[# of lines]>           Error Log
  
  stop                             Daemon beenden
\"\"\")
""".format(path=path)

	f = open("/usr/bin/aq","w") 
	f.write(str(inputpy))
	f.close()

	os.system ("chmod +x /usr/bin/aq")
	print ("Erfolgreich!")
	print ("Usage: aq <command> [<args>]\n")

except Exception as e:
	print ("Fehlgeschlagen.\n " + str(e))

try:
	print ("Richte Systemd Daemon ein...")
	systemd = """[Unit]
Description=Fischlicht
After=multi-user.target

[Service]
Type=simple
ExecStart={path}/daemon.py
ExecStop=/usr/bin/aq stop
User=pi
WorkingDirectory={path}
Restart=on-failure

[Install]
WantedBy=multi-user.target""".format(path=path)

	f = open("/etc/systemd/system/fischlicht.service","w") 
	f.write(str(systemd))
	f.close()

	os.system ("chmod +x {}/daemon.py".format(path))
	
	print ("Aktiviere Systemd Daemon...")
	
	os.system ("systemctl enable fischlicht.service")
	os.system ("systemctl daemon-reload")
	
	print ("Erfolgreich!")
	print ("Usage: sudo systemctl <start|stop|restart|status|...> fischlicht\n")
	
except Exception as e:
	print ("Fehlgeschlagen.\n " + str(e))
	
if os.path.isfile("{}/config.ini".format(path)) == False:
	try:
		print ("Erstelle config...")
		configini="""# Fischlicht Config File #

# BCM Pinbezeichnung

[general]
interval = 300
#i2c-bus = 1

[ph]
active = 1
#address = 0x48
ph_value = 7.3
outlet = 4

[led]
#latch = 8
#data = 10
#clock = 11
#			R	G	B
assign = 4, 5, 3,
		0, 1, 2,
		16, 17, 15,
		12, 13, 14,
		9, 10, 11, 
		18, 20, 19,
		22, 21, 23,
		6, 7, 8
#maxstep = 10
#period = 0.2
			
[temp]
active=1
# sensor-id=["name" [, low_warning, high_warning [, low_alert, high_alert]]
28-000005986837 = hinten, 26.5, 28.5, 23, 31
28-000005985d20 = vorn, 26.5, 28.5, 23, 31 
28-000005af42fe = raum, 16, 28
# Temp-Sensor mit Bezeichnung "case" steuert den Luefter [low_warning = Lüfter an, low_alert = Lüfter aus] 
10-000802e4371a = case, 30, 40, 28, 50

[outlet]
#devices: A = 1, B = 2, C = 4, D = 8, E = 16  
code = 1,1,1,1,1 
pin = 17

[fan]
pin = 18

[flow]
active = 0
pin = 5

[power]
# modes: gpio, outlet 
mode = gpio 
pin = 22

[ina219]
# voltage/current sensor
active = 1
#address = 0x40
#config_register = 0x1F, 0xFF
#calib_register = 0x14, 0xF8

[pcf8591]
# A/D Converter
#active = 0
#address = 0x4f

[telebot]
active = 0
bot_id = 
user_id = 
"""

		f = open("{}/config.ini".format(path),"w") 
		f.write(str(configini))
		f.close()
		print ("Erfolgreich!\n")

	except Exception as e:
		print ("Fehlgeschlagen.\n " + str(e))
		
if os.path.isfile("{}/spi/lichtprogramme.py".format(path)) == False:
	try:
		print ("Erstelle Lichtprogramm Config (/spi/lichtprogramme.py)...")
		configlp="""#Lichtprogramme
# !ZUORDUNG AM ENDE BEACHTEN!

off=0
on=4095

#Beispiele:
#Normale Beleuchtung
rt	=	4095
gr	=	1900
bl	=	1700
normal = 	   [rt,		 gr,	 bl,	#Lampe 1: 1. Reihe, rechts
				rt,		 gr,	 bl,	#Lampe 2: 1. Reihe, links
				rt,		 gr,	 bl,	#Lampe 3: 2. Reihe, rechts
				rt,		 gr,	 bl,	#Lampe 4: 2. Reihe, mittig
				rt,		 gr,	 bl,	#Lampe 5: 2. Reihe, links
				rt,		 gr,	 bl,	#Lampe 6: 3. Reihe
				rt,		 gr,	 bl]	#Lampe 7: 4. Reihe
							
				
#Mondlicht
mondlicht =	   [10,	 	10,	 	80,		#Lampe 1: 1. Reihe, rechts
				10,	 	10,	 	80,		#Lampe 2: 1. Reihe, links
				20,	 	20,	 	200,	#Lampe 3: 2. Reihe, rechts
				20,	 	20,	 	200,	#Lampe 4: 2. Reihe, mittig
				20,		20,	 	200,	#Lampe 5: 2. Reihe, links
				60,		30,	 	600,	#Lampe 6: 3. Reihe
				60,	 	30,	 	500]	#Lampe 7: 4. Reihe

					
#Mondlicht - Verlauf	
mondschein =  [[10,	 	10,	 	80,		#Lampe 1: 1. Reihe, rechts
				10,	 	10,	 	80,		#Lampe 2: 1. Reihe, links
				20,	 	20,		200,	#Lampe 3: 2. Reihe, rechts
				20,	 	20,	 	200,	#Lampe 4: 2. Reihe, mittig
				120,	60,	 	200,	#Lampe 5: 2. Reihe, links
				60,	 	30,	 	600,	#Lampe 6: 3. Reihe
				60,	 	30,	 	500],	#Lampe 7: 4. Reihe

			   [10,	 	10,	 	80,		#Lampe 1: 1. Reihe, rechts
				10,	 	10,	 	80,		#Lampe 2: 1. Reihe, links
				20,	 	20,	 	200,	#Lampe 3: 2. Reihe, rechts
				20,	 	20,	 	200,	#Lampe 4: 2. Reihe, mittig
				20,	 	20,	 	200,	#Lampe 5: 2. Reihe, links
				60,	 	30,	 	600,	#Lampe 6: 3. Reihe
				340,	240,	500],	#Lampe 7: 4. Reihe
				
			   [10,	 	10,	 	80,		#Lampe 1: 1. Reihe, rechts
				10,	 	10,		80,		#Lampe 2: 1. Reihe, links
				120,	60,	 	200,	#Lampe 3: 2. Reihe, rechts
				20,	 	20,	 	200,	#Lampe 4: 2. Reihe, mittig
				20,	 	20,	 	200,	#Lampe 5: 2. Reihe, links
				60,	 	30,	 	600,	#Lampe 6: 3. Reihe
				60,	 	30,	 	500]]	#Lampe 7: 4. Reihe
						
#Wolkig - Verlauf
# -1 = Wert des urspruenglichen Lichtprogrammes	

wolkig =	  [[0,	 	 0,	 	 0,		#Lampe 1: 1. Reihe, rechts
				-1,	 	-1,		-1,		#Lampe 2: 1. Reihe, links
				0,	 	 0,		 0,		#Lampe 3: 2. Reihe, rechts
				-1,	 	-1,	 	-1,		#Lampe 4: 2. Reihe, mittig
				-1,	 	-1,	 	-1,		#Lampe 5: 2. Reihe, links
				-1,	 	-1,	 	-1,		#Lampe 6: 3. Reihe
				-1,	 	-1,	 	-1],	#Lampe 7: 4. Reihe

			   [ 0,	 	 0,		 0,		#Lampe 1: 1. Reihe, rechts
				-1,	 	-1,	 	-1,		#Lampe 2: 1. Reihe, links
				-1,	 	-1,	 	-1,		#Lampe 3: 2. Reihe, rechts
				0,	 	 0,		 0,		#Lampe 4: 2. Reihe, mittig
				0,	 	 0,		 0,		#Lampe 5: 2. Reihe, links
				-1,	 	-1,		-1,		#Lampe 6: 3. Reihe
				-1,	 	-1,	 	-1],	#Lampe 7: 4. Reihe
						
#...
				
			   [-1,	 	-1,		-1,		#Lampe 1: 1. Reihe, rechts
				-1,	 	-1,	 	-1,		#Lampe 2: 1. Reihe, links
				-1,	 	-1,	 	-1,		#Lampe 3: 2. Reihe, rechts
				-1,	 	-1,	 	-1,		#Lampe 4: 2. Reihe, mittig
				-1,	 	-1,	 	-1,		#Lampe 5: 2. Reihe, links
				-1,	 	-1,	 	-1,		#Lampe 6: 3. Reihe
				-1,	 	-1,	 	-1]]	#Lampe 7: 4. Reihe
				
#"Name zum Aufrufen" : Zugehöriges Array
zuordnung =		 {	"normal"		:	normal			,
				"mondlicht"			:	mondlicht		,
				"mondschein"		:	mondschein		,
				"wolkig"			:	wolkig			}
"""

		f = open("{}/spi/lichtprogramme.py".format(path),"w") 
		f.write(str(configlp))
		f.close()
		print ("Erfolgreich!\n")

	except Exception as e:
		print ("Fehlgeschlagen.\n " + str(e))		


try: 
	print ("Lege Logfiles an...")
	os.system("mkdir /var/log/Fischlicht")
	os.system("touch /var/log/Fischlicht/daemon.log")
	os.system("touch /var/log/Fischlicht/error.log")

	os.system("chown -cR pi:pi /var/log/Fischlicht/")
	
	print ("Erfolgreich!\n")
	
except Exception as e:
	print ("Fehlgeschlagen.\n " + str(e))
		
print ("Setup abgeschlossen")
