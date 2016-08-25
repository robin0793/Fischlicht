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

if len(sys.argv)>1:
	
	allarguments = sys.argv[1] 
	for e in range(2,len(sys.argv)):
		allarguments = "{{}} {{}}".format(allarguments, sys.argv[e]) 


	if sys.argv[1]=="ledm":
		print ("Coming soon... ;)")
	elif sys.argv[1]=="daemon":
		os.system("screen -S FISCHLICHT -d -m python3 {path}/daemon.py")
	else:
		os.system("echo {{}} > {path}/pipe".format(allarguments))
else:
	print(\"\"\"~~~ FISCHLICHT ~~~

Usage: aq <command> [<args>]

Commands:
  led  [lichtprogramm] [dauer]  Aendern des Lichtprogrammes
  nt   [0|1]                    Netzteil schalten
  fan  [0-100]                  Lüfterdrehzahl setzen [%]
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
	print ("Usage: sudo systemctl <start|stop|restart|status|...> fischlicht.service\n")
	
except Exception as e:
	print ("Fehlgeschlagen.\n " + str(e))
	
if os.path.isfile("{}/config.ini".format(path)) == False:
	try:
		print ("Erstelle config ...")
		configini="""# Fischlicht Config File #

# BCM Pinbezeichnung

[general]
interval = 300
i2c-bus = 1

[ph]
active = 1
address = 0x48
ph_value = 7.3
outlet = 4

[led]
latch = 8
data = 10
clock = 11
#			R	G	B
assign = 4, 5, 3,
		0, 1, 2,
		16, 17, 15,
		12, 13, 14,
		9, 10, 11, 
		18, 20, 19,
		22, 21, 23,
		6, 7, 8
maxstep = 10
period = 0.2
			
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

[power]
# modes: gpio, outlet 
mode = gpio 
pin = 22

[ina219]
# voltage/current sensor
active = 1
address = 0x40
config_register = 0x1F, 0xFF
calib_register = 0x14, 0xF8

[pcf8591]
# A/D Converter
active = 0
address = 0x4f

[telebot]
active = 0
bot_id = 
user_id = 
"""

		f = open("{}/config.ini".format(path),"w") 
		f.write(str(configini))
		f.close()
		print ("Erfolgreich!")

	except Exception as e:
		print ("Fehlgeschlagen.\n " + str(e))

print()
print ("Setup abgeschlossen")
