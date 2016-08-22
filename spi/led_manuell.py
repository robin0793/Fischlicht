#!/usr/bin/env python3

#IMPORT
import time
import RPi.GPIO as GPIO
import sys
import pickle
from os import path
from numpy import array
from numpy import array_equal

#GPIO INIT 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(8, GPIO.OUT)   #Latch
GPIO.setup(10, GPIO.OUT)   #Data
GPIO.setup(11, GPIO.OUT)   #Clock

path = path.dirname(path.realpath(__file__))

#LICHTPROGRAMME
import lichtprogramme as lp

#FUNKTION PWM 
def pwm(intens):
	GPIO.output(8, GPIO.LOW)   #Latch low

	for output in range(0,24):
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
	for v in range(0,len(intens_dy)):
		for b in range(0,len(intens_ac)):
			if intens_dy[v][b] == -1:
				intens_dy[v][b] = intens_ac[b]
	return intens_dy


#MAIN
try:
			
	if len(sys.argv) > 1:
		
		intens=[]		
		for h in range (1,len(sys.argv),1):
			intens.append(int(sys.argv[h]))

#ARRAY ANPASSEN - Legt Stelle fest, in der der Wert des Lichtprogrammes im Array stehen muss, d.h. auf welchen Kanal der Wert übertragen werden soll

#						R	G	B
		zuordnung_tlc = [	4,	5,	3,	#Lampe 1: 1. Reihe, rechts
							0,	1,	2,	#Lampe 2: 1. Reihe, links
							16,	17,	15,	#Lampe 3: 2. Reihe, rechts
							12,	13,	14,	#Lampe 4: 2. Reihe, mittig
							9,	10,	11,	#Lampe 5: 2. Reihe, links
							18,	20,	19,	#Lampe 6: 3. Reihe
							22,	21,	23,	#Lampe 7: 4. Reihe
							6,	7,	8]	#Nicht belegt

		intens_wanted=[0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0]
		for j in range(0,len(intens)):
			intens_wanted[zuordnung_tlc[j]] = intens[j] #zuordnung_tlc[j] ist die Stelle, an die der Wert im neuen Array liegen soll		
		intens_wanted=array(intens_wanted)
		
	else:
		print ("Keine Argumente")
		quit()

#BERECHNUNG INTERVALLE
	dauer = 1
	steps = 1

	pwm(intens_wanted)
	print ("ok")


except KeyboardInterrupt:
	print ("Programm unterbrochen")
	quit()