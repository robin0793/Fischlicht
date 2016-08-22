#!/usr/bin/env python3

#IMPORT

import RPi.GPIO as GPIO
import time
from datetime import datetime
import pickle 
from os import path
from numpy import array, array_equal, subtract, absolute, amax



#GPIO INIT 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(8, GPIO.OUT)   #Latch
GPIO.setup(10, GPIO.OUT)   #Data
GPIO.setup(11, GPIO.OUT)   #Clock

path = path.dirname(path.realpath(__file__))

#LICHTPROGRAMME
if __name__ == "__main__":
	import lichtprogramme as lp
else:	
	import spi.lichtprogramme as lp

#ZUORDNUNG KOMMANDOZEILE > LICHTPROGRAMM
zuordnung =		 {	"normal"		:	lp.normal			,
				"mondlicht"			:	lp.mondlicht		,
				"mondschein"		:	lp.mondschein		,
				"sonnenaufgang"		:	lp.sonnenaufgang	,
				"sonnenunter"		:	lp.sonnenunter		,
				"max"				:	lp.max				,
				"warm"				:	lp.warm				,
				"wolkig"			:	lp.wolkig			,
				"dim"				:	lp.dim				}

#ARRAY ANPASSEN - Legt Stelle fest, in der der Wert des Lichtprogrammes im Array stehen muss, d.h. auf welchen Kanal der Wert übertragen werden soll
#						R	G	B
zuordnung_tlc =		 [	4,	5,	3,	#Lampe 1: 1. Reihe, rechts
						0,	1,	2,	#Lampe 2: 1. Reihe, links
						16,	17,	15,	#Lampe 3: 2. Reihe, rechts
						12,	13,	14,	#Lampe 4: 2. Reihe, mittig
						9,	10,	11,	#Lampe 5: 2. Reihe, links
						18,	20,	19,	#Lampe 6: 3. Reihe
						22,	21,	23,	#Lampe 7: 4. Reihe
						6,	7,	8]	#Nicht belegt

#FUNKTION UEBERTRAGUNG 
def transfer(intens):
	
	GPIO.output(8, GPIO.LOW)   #Latch low
	ubound = len(intens) 
	for output in range(0,ubound):
		for bit in range(11,-1, -1):
			GPIO.output(11, GPIO.LOW)   #Clock low
			
			if int(round(intens[output])) & (1 << bit):
				GPIO.output(10, GPIO.HIGH) #Data high
			else:
				GPIO.output(10, GPIO.LOW) #Data low
			GPIO.output(11, GPIO.HIGH)   #Clock high
	 
	GPIO.output(11, GPIO.LOW)   #Clock low

	GPIO.output(8, GPIO.HIGH)   #Latch high
	GPIO.output(8, GPIO.LOW)   #Latch low


def dynamic(intens_dy, intens_ac):
	
	for b in range(0,len(intens_ac)):
		if intens_dy[b] == -1: intens_dy[b] = intens_ac[b]
		
	return intens_dy

#MAIN
def setled(arg_array): # 0 = Lichtprogramm, 1 = Dauer
	try:
		f = open(path+"/lichtwerte.db", "rb")
		intens_now = pickle.load(f)
		f.close()



		if len(arg_array) < 2:	
			print(time.strftime("[%Y-%m-%d %H:%M]"), "[LEDS] Aktuelles Programm neu setzen")
			transfer(intens_now)
			return None
		
		if arg_array[1] in zuordnung:
			intens_set=zuordnung[arg_array[1]]
			print(time.strftime("[%Y-%m-%d %H:%M]"), "[LEDS] Starte Lichtprogramm:", arg_array[1])
		else:
			intens_set=lp.aus
			
	#ANPASSUNG FÜR VERLÄUFE

		if type(intens_set[0])==list:
			multi = len(intens_set)-1
		else:
			multi = 0
		
		intens_orig = intens_now
		
		for k in range(0, multi+1):
			
			if multi != 0:
				intens = intens_set[k]
			else: 
				intens = intens_set

		#ARRAY ANPASSEN - Legt Stelle fest, in der der Wert des Lichtprogrammes im Array stehen muss, d.h. auf welchen Kanal der Wert übertragen werden soll


			intens_wanted=[0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0]
			for j in range(0,len(intens)):
				intens_wanted[zuordnung_tlc[j]] = intens[j] #zuordnung_tlc[j] ist die Stelle, an die der Wert im neuen Array liegen soll		
			intens_wanted=dynamic(array(intens_wanted),intens_orig)
			
			
			
			if len(intens_wanted) != len(intens_now):
				
				transfer(intens_wanted)
				f = open(path+"/lichtwerte.db", "wb")
				pickle.dump(intens_wanted,f)
				f.close()
				quit()
			
			if array_equal (intens_wanted, intens_now) == True:
				print(time.strftime("[%Y-%m-%d %H:%M]"), "[LEDS] Aktuelles Programm neu setzen")
				transfer(intens_now)
				quit()
				
		#BERECHNUNG INTERVALLE
			
			dauer=10
			if len(arg_array) > 2:
				try: 
					zeit=int(arg_array[2])
					dauer = zeit*60/(1+multi) #in Sekunden
				except:
					print(time.strftime("[%Y-%m-%d %H:%M]"), "[LEDS] Falsche Zeitangabe")		

			maxstep = 10 # Maximale Differenz der Farbwerte zwischen zwei schritten
			
			if type(intens_wanted[0])==list:
				intens_maxdiff = int(amax(absolute(subtract(intens_wanted[0], intens_now)))) # Maximum des Differenzbetrags
				period = dauer * maxstep / (intens_maxdiff * (len(intens_wanted)))
			else:
				intens_maxdiff = int(amax(absolute(subtract(intens_wanted, intens_now)))) # Maximum des Differenzbetrags
				period = dauer * maxstep / intens_maxdiff #Periodendauer d.h. Zeit zwischen den Schritten
			
			if period < .2:		#Minimale Periodendauer ist 200 ms, da Übertragung bis zu 150 ms dauert ( + Sicherheit)
				period = .2
				maxstep = period * intens_maxdiff / dauer	#Schrittweite anpassen
			steps = int(round(dauer / period))	
			

			print(time.strftime("[%Y-%m-%d %H:%M]"), "[LEDS] Dauer: ", dauer)
			print(time.strftime("[%Y-%m-%d %H:%M]"), "[LEDS] Schrittweite: ", maxstep)
			print(time.strftime("[%Y-%m-%d %H:%M]"), "[LEDS] Periodendauer: ", period)
			print(time.strftime("[%Y-%m-%d %H:%M]"), "[LEDS] Anzahl Übertragungen:", steps)


				
			intens_raise=(intens_wanted-intens_now)/steps

			for z in range(1,steps,1):
				t_start = datetime.now()
				intens_step=intens_now+z*intens_raise
				transfer(intens_step)
				t_end = datetime.now()
				delta = t_end - t_start
				time.sleep(period - delta.total_seconds())
			transfer(intens_wanted)
			print(time.strftime("[%Y-%m-%d %H:%M]"), "[LEDS] Lichtprogramm abgeschlossen:", arg_array[1])
			print()
			f = open(path+"/lichtwerte.db", "wb")
			pickle.dump(intens_wanted,f)
			f.close()
			intens_now = intens_wanted
		
	except KeyboardInterrupt:
		print(time.strftime("[%Y-%m-%d %H:%M]"), "[LEDS] Programm unterbrochen")
		quit()

	
if __name__ == "__main__":
	from sys import argv
	if len(argv) > 1:
		setled(argv)
	