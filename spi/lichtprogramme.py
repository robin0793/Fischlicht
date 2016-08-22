#Lichtprogramme
off=0
on=4095

rot=0
gruen=0
blau=0

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
							

#Gedimmtes Licht
rt	=	2300
gr	=	1000
bl	=	1000
dim =		   [rt,		 gr,	 bl,	#Lampe 1: 1. Reihe, rechts
				rt,		 gr,	 bl,	#Lampe 2: 1. Reihe, links
				rt,		 gr,	 bl,	#Lampe 3: 2. Reihe, rechts
				rt,		 gr,	 bl,	#Lampe 4: 2. Reihe, mittig
				rt,		 gr,	 bl,	#Lampe 5: 2. Reihe, links
				rt,		 gr,	 bl,	#Lampe 6: 3. Reihe
				rt,		 gr,	 bl]	#Lampe 7: 4. Reihe
							
							
#Warmes Licht - Abend
rt	=	4095
gr	=	1300
bl	=	450
warm =	   	   [rt,		 gr,	 bl,	#Lampe 1: 1. Reihe, rechts
				rt,		 gr,	 bl,	#Lampe 2: 1. Reihe, links
				rt,		 gr,	 bl,	#Lampe 3: 2. Reihe, rechts
				rt,		 gr,	 bl,	#Lampe 4: 2. Reihe, mittig
				rt,		 gr,	 bl,	#Lampe 5: 2. Reihe, links
				rt,		 gr,	 bl,	#Lampe 6: 3. Reihe
				rt,		 gr,	 bl]	#Lampe 7: 4. Reihe


#Ausgeschalten
rt	=	0
gr	=	0
bl	=	0
aus =		  [[rt,		 gr,	 bl,	#Lampe 1: 1. Reihe, rechts
				rt,		 gr,	 bl,	#Lampe 2: 1. Reihe, links
				rt,		 gr,	 bl,	#Lampe 3: 2. Reihe, rechts
				20,		 20,	 200,	#Lampe 4: 2. Reihe, mittig
				rt,		 gr,	 bl,	#Lampe 5: 2. Reihe, links
				rt,		 gr,	 bl,	#Lampe 6: 3. Reihe
				rt,		 gr,	 bl],	#Lampe 7: 4. Reihe

			   [rt,		 gr,	 bl,	#Lampe 1: 1. Reihe, rechts
				rt,		 gr,	 bl,	#Lampe 2: 1. Reihe, links
				rt,		 gr,	 bl,	#Lampe 3: 2. Reihe, rechts
				rt,		 gr,	 bl,	#Lampe 4: 2. Reihe, mittig
				rt,		 gr,	 bl,	#Lampe 5: 2. Reihe, links
				rt,		 gr,	 bl,	#Lampe 6: 3. Reihe
				rt,		 gr,	 bl]]	#Lampe 7: 4. Reihe

							
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

				
#Sonnenaufgang
sonnenaufgang =[2000, 	200, 	0,		#Lampe 1: 1. Reihe, rechts
				2000, 	200,	0,		#Lampe 2: 1. Reihe, links
				2700, 	100,	0,		#Lampe 3: 2. Reihe, rechts
				3500, 	100,	0,		#Lampe 4: 2. Reihe, mittig
				2700, 	100,	0,		#Lampe 5: 2. Reihe, links
				4095, 	100,	0,		#Lampe 6: 3. Reihe
				4095, 	100,	0]		#Lampe 7: 4. Reihe
				
#Sonnenuntergang						
sonnenunter = [[2000, 	200, 	80,		#Lampe 1: 1. Reihe, rechts
				2000, 	200,	80,		#Lampe 2: 1. Reihe, links
				2700, 	150,	80,		#Lampe 3: 2. Reihe, rechts
				3200, 	150,	80,		#Lampe 4: 2. Reihe, mittig
				2700, 	150,	80,		#Lampe 5: 2. Reihe, links
				3600, 	120,	80,		#Lampe 6: 3. Reihe
				3600, 	120,	80],		#Lampe 7: 4. Reihe
				
			   [400, 	10, 	80,		#Lampe 1: 1. Reihe, rechts
				400, 	10,		80,		#Lampe 2: 1. Reihe, links
				20, 	20,		1500,	#Lampe 3: 2. Reihe, rechts
				2700, 	150,	80,		#Lampe 4: 2. Reihe, mittig
				20, 	20,		1500,	#Lampe 5: 2. Reihe, links
				200, 	10,		80,		#Lampe 6: 3. Reihe
				1200, 	20,		200]]

#Maximale Helligkeit
rt	=	4095
gr	=	4095
bl	=	4095
max =	   	   [rt,		 gr,	 bl,	#Lampe 1: 1. Reihe, rechts
				rt,		 gr,	 bl,	#Lampe 2: 1. Reihe, links
				rt,		 gr,	 bl,	#Lampe 3: 2. Reihe, rechts
				rt,		 gr,	 bl,	#Lampe 4: 2. Reihe, mittig
				rt,		 gr,	 bl,	#Lampe 5: 2. Reihe, links
				rt,		 gr,	 bl,	#Lampe 6: 3. Reihe
				rt,		 gr,	 bl]	#Lampe 7: 4. Reihe
							
							
#Wolkig - Verlauf	
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
						
			   [-1,	 	-1,	 	-1,		#Lampe 1: 1. Reihe, rechts
				-1,	 	-1,	 	-1,		#Lampe 2: 1. Reihe, links
				-1,	 	-1,	 	-1,		#Lampe 3: 2. Reihe, rechts
				0,	 	 0,		 0,		#Lampe 4: 2. Reihe, mittig
				0,	 	 0,		 0,		#Lampe 5: 2. Reihe, links
				0,	 	 0,		 0,		#Lampe 6: 3. Reihe
				-1,	 	-1,	 	-1],	#Lampe 7: 4. Reihe
				
			   [-1,	 	-1,	 	-1,		#Lampe 1: 1. Reihe, rechts
				0,	 	 0,		 0,		#Lampe 2: 1. Reihe, links
				0,	 	 0,		 0,		#Lampe 3: 2. Reihe, rechts
				-1,	 	-1,		-1,		#Lampe 4: 2. Reihe, mittig
				-1,	 	-1,	 	-1,		#Lampe 5: 2. Reihe, links
				0,	 	 0,		 0,		#Lampe 6: 3. Reihe
				-1,	 	-1,	 	-1],	#Lampe 7: 4. Reihe
				
			   [ 0,	 	 0,		 0,		#Lampe 1: 1. Reihe, rechts
				-1,	 	-1,	 	-1,		#Lampe 2: 1. Reihe, links
				-1,	 	-1,	 	-1,		#Lampe 3: 2. Reihe, rechts
				0,	 	 0,		 0,		#Lampe 4: 2. Reihe, mittig
				-1,	 	-1,	 	-1,		#Lampe 5: 2. Reihe, links
				-1,	 	-1,	 	-1,		#Lampe 6: 3. Reihe
				0,	 	 0,		 0],	#Lampe 7: 4. Reihe
								
			   [-1,	 	-1,	 	-1,		#Lampe 1: 1. Reihe, rechts
				0,	 	 0,		 0,		#Lampe 2: 1. Reihe, links
				0,	 	 0,		 0,		#Lampe 3: 2. Reihe, rechts
				0,	 	 0,		 0,		#Lampe 4: 2. Reihe, mittig
				-1,	 	-1,	 	-1,		#Lampe 5: 2. Reihe, links
				-1,	 	-1,	 	-1,		#Lampe 6: 3. Reihe
				0,	 	 0,		 0],	#Lampe 7: 4. Reihe
				
			   [ 0,	 	 0,		 0,		#Lampe 1: 1. Reihe, rechts
				-1,	 	-1,	 	-1,		#Lampe 2: 1. Reihe, links
				0,	 	 0,		 0,		#Lampe 3: 2. Reihe, rechts
				-1,	 	-1,	 	-1,		#Lampe 4: 2. Reihe, mittig
				-1,	 	-1,	 	-1,		#Lampe 5: 2. Reihe, links
				0,	 	 0,		 0,		#Lampe 6: 3. Reihe
				-1,		-1,	 	-1],	#Lampe 7: 4. Reihe
				
			   [-1,	 	-1,	 	-1,		#Lampe 1: 1. Reihe, rechts
				-1,	 	-1,	 	-1,		#Lampe 2: 1. Reihe, links
				-1,	 	-1,	 	-1,		#Lampe 3: 2. Reihe, rechts
				-1,	 	-1,	 	-1,		#Lampe 4: 2. Reihe, mittig
				0,	 	 0,		 0,		#Lampe 5: 2. Reihe, links
				-1,	 	-1,	 	-1,		#Lampe 6: 3. Reihe
				0,	 	 0,		 0],	#Lampe 7: 4. Reihe
				
			   [-1,	 	-1,		-1,		#Lampe 1: 1. Reihe, rechts
				-1,	 	-1,	 	-1,		#Lampe 2: 1. Reihe, links
				-1,	 	-1,	 	-1,		#Lampe 3: 2. Reihe, rechts
				-1,	 	-1,	 	-1,		#Lampe 4: 2. Reihe, mittig
				-1,	 	-1,	 	-1,		#Lampe 5: 2. Reihe, links
				-1,	 	-1,	 	-1,		#Lampe 6: 3. Reihe
				-1,	 	-1,	 	-1]]	#Lampe 7: 4. Reihe