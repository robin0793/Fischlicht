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


print ("Setup abgeschlossen")
