import math

#Sacar cosas cercas del punto inicio y punto fin 
def menorDistancia(Punto1, Punto2, distancia):
	(x1,y1)= Punto1
	(x2,y2)= Punto2
	
	latitudDif= Punto2[0]-Punto1[0]
	longitudRadio = Punto2[1]-Punto1[1]

	latitudDifMetros= (latitudDif*111)*1000
	longitudRadioMetros= (longitudRadio*111)*1000
	hip = math.sqrt( (latitudDifMetros)*(latitudDifMetros)+(longitudRadioMetros)*(longitudRadioMetros))
	hipKm =hip/1000
	if hipKm <= distancia:
		return True 
	
def getPuntosCercanos(Punto,distancia, ListaSitios):
	#(x,y) = Punto 

	PuntosCercanosList= list()

	for (Id,Tipo,Nombre,la,lon) in ListaSitios:
		if(menorDistancia((la,lon),Punto,distancia)):
			PuntosCercanosList.append([Id,Tipo,Nombre,la,lon])

	return PuntosCercanosList







Lista= [[1,"Biblioteca","Biblioteca1", 37.357924, -5.986320], [2,"Museo","Museo1",37.362922, -5.975878]]
PuntoA = (37.355508, -5.987698)
print(getPuntosCercanos(PuntoA,50,Lista))