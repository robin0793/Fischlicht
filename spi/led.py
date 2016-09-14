#!/usr/bin/env python3

#IMPORT

import RPi.GPIO as GPIO
import time
from datetime import datetime
import pickle 
from os import path
from numpy import array, array_equal, subtract, absolute, amax, dtype
import logging

if __name__ == "__main__":
	import lichtprogramme as lp
else:	
	import spi.lichtprogramme as lp

log = logging.getLogger("daemon")
errlog = logging.getLogger("error")

path = path.dirname(path.realpath(__file__))

class led():

	def __init__(self, latch = 8, data = 10, clock = 11, zuordnung = [0,1,2, 3,4,5, 6,7,8, 9,10,11, 12,13,14, 15,16,17, 18,19,20, 21,22,23], aktiv = "aus", intens = [0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0], maxstep = 10, period = 0.2):
		self.latch = latch
		self.data = data
		self.clock = clock

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		
		GPIO.setup(self.latch, GPIO.OUT)   #Latch
		GPIO.setup(self.data, GPIO.OUT)   #Data
		GPIO.setup(self.clock, GPIO.OUT)   #Clock
		
		self.zuordnung = zuordnung
		self.aktiv = aktiv
		self.maxstep = maxstep
		self.period = period
		self.running = 0
		
		self.intens = array(intens)
		
	def transfer(self, intens):
		GPIO.output(self.latch, GPIO.LOW)   #Latch low
		ubound = len(intens) 
		for output in range(0,ubound):
			for bit in range(11,-1, -1):
				GPIO.output(self.clock, GPIO.LOW)   #Clock low
				
				if int(round(intens[output])) & (1 << bit):
					GPIO.output(self.data, GPIO.HIGH) #Data high
				else:
					GPIO.output(self.data, GPIO.LOW) #Data low
				GPIO.output(self.clock, GPIO.HIGH)   #Clock high
		 
		GPIO.output(self.clock, GPIO.LOW)   #Clock low

		GPIO.output(self.latch, GPIO.HIGH)   #Latch high
		GPIO.output(self.latch, GPIO.LOW)   #Latch low


	def dynamic(self, intens_dy, intens_ac):
		
		for b in range(0,len(intens_ac)):
			if intens_dy[b] == -1: intens_dy[b] = intens_ac[b]
			
		return intens_dy

	def setled(self, arg_array): # 1 = Lichtprogramm, 2 = Dauer, 3 = Priorität
		try:
			
			
			prio = int(arg_array[3]) if len(arg_array) > 3 else 2
			if prio <= self.running:
				log.warn("Lichprogramm mit höherer Priorität ({}) läuft bereits".format(self.running))
				return 0

			self.running = prio

			
			# Nach Lichtprogramm mit passendem Name suchen
			if type(arg_array[1]) is list:
				intens_set = arg_array[1]
			else:
				try:
					intens_set = eval("lp.{}".format(arg_array[1]))
					log.info("Starte Lichtprogramm: {}".format(arg_array[1]))
					self.aktiv = arg_array[1]
				except NameError:
					log.warn("Lichtprogramm \"{}\" nicht vorhanden".format(arg_array[1]))
					self.running = 0
					return 0
				except:
					try: 
						intens_set = array(list(map(float, arg_array[1].split(","))))
					except:
						log.warn("Fehlerhafte Eingabe Lichtprogramm")
						self.running = 0
						return 0
				
		#ANPASSUNG FÜR VERLÄUFE

			if type(intens_set[0])==list:
				multi = len(intens_set)-1
			else:
				multi = 0
			intens_orig = self.intens
			
			for k in range(0, multi+1):
				
				if multi != 0:
					intens = intens_set[k]
				else: 
					intens = intens_set

			#ARRAY ANPASSEN - Legt Stelle fest, in der der Wert des Lichtprogrammes im Array stehen muss, d.h. auf welchen Kanal der Wert übertragen werden soll

				intens_wanted=[0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0]
				
				for j in range(0,len(intens)):
					intens_wanted[self.zuordnung[j]] = intens[j] #zuordnung_tlc[j] ist die Stelle, an die der Wert im neuen Array liegen soll	
					
				intens_wanted = self.dynamic(array(intens_wanted),intens_orig)
				
				
				while len(intens_wanted) > len(self.intens):
					self.intens.append(0)
				
				if array_equal (intens_wanted, self.intens) == True:
					log.info("Aktuelles Programm neu setzen")
					self.transfer(intens_wanted)
					self.running = 0
					return 1
					
			#BERECHNUNG INTERVALLE
				
				dauer=10
				if len(arg_array) > 2:
					try: 
						zeit=int(arg_array[2])
						dauer = zeit*60/(1+multi) #in Sekunden
					except:
						log.warn("Falsche Zeitangabe")		

				maxstep = self.maxstep # Maximale Differenz der Farbwerte zwischen zwei schritten
				
				if type(intens_wanted[0])==list:
					intens_maxdiff = int(amax(absolute(subtract(intens_wanted[0], self.intens)))) # Maximum des Differenzbetrags
					period = dauer * maxstep / (intens_maxdiff * (len(intens_wanted)))
				else:
					intens_maxdiff = int(amax(absolute(subtract(intens_wanted, self.intens)))) # Maximum des Differenzbetrags
					period = dauer * maxstep / intens_maxdiff #Periodendauer d.h. Zeit zwischen den Schritten
				
				if period < self.period:		#Minimale Periodendauer ist 200 ms, da Übertragung bis zu 150 ms dauert ( + Sicherheit)
					period = self.period
					maxstep = period * intens_maxdiff / dauer	#Schrittweite anpassen
				steps = int(round(dauer / period))	
				

				log.info("Dauer: {}".format(dauer))
				log.info("Schrittweite: {}".format(maxstep))
				log.info("Periodendauer: {}".format(period))
				log.info("Anzahl Übertragungen: {}".format(steps))
				
				intens_raise=(intens_wanted-self.intens)/steps

				
				for z in range(1,steps,1):
					t_start = datetime.now()
					self.intens = self.intens + intens_raise
					self.transfer(self.intens)
					t_end = datetime.now()
					delta = t_end - t_start
					time.sleep(period - delta.total_seconds())
					if prio < self.running: 
						log.info("Lichprogramm {} unterbrochen, da LP mit höherer Priorität vorhanden".format(arg_array[1]))
						return 2
				self.intens=intens_wanted
				self.transfer(self.intens)
				log.info("Lichtprogramm abgeschlossen:{}".format(arg_array[1]))
				print()

				self.intens = intens_wanted
				self.running = 0
				
		except KeyboardInterrupt:
			log.warn("Programm unterbrochen")
			self.running = 0
			
		except Exception as e:
			log.warn("Programm unterbrochen. Fehler: {}".format(e))
			self.running = 0