#!/usr/bin/python3

import os
import sys

if not os.geteuid() == 0:
	print("Run as root!")
	exit()
	
path = os.path.dirname(os.path.realpath(__file__))

inputpy = """#!/usr/bin/python3

import sys
import os

if len(sys.argv)>1:
	
	allarguments = sys.argv[1] 
	for e in range(2,len(sys.argv)):
		allarguments = "{{}} {{}}".format(allarguments, sys.argv[e]) 
	print (allarguments)

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

