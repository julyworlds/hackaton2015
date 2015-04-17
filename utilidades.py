import math

def getDistancia(Punto1, Punto2):
	(x1,y1)= Punto1
	(x2,y2)= Punto2

	latitudDif= Punto2[0]-Punto1[0]
	longitudRadio = Punto2[1]-Punto1[1]

	latitudDifMetros= (latitudDif*111)*1000
	longitudRadioMetros= (longitudRadio*111)*1000
	hip = math.sqrt( (latitudDifMetros)*(latitudDifMetros)+(longitudRadioMetros)*(longitudRadioMetros))
	return hip

#Sacar cosas cercas del punto inicio y punto fin 
def menorDistancia(Punto1, Punto2, distancia):
	hip = getDistancia(Punto1,Punto2)
	if hip <= distancia:
		return hip
	else:
		return None

def getPuntosCercanos(Punto, distancia, ListaSitios):
	PuntosCercanosList= list()

	for (Id,Tipo,Nombre,la,lon) in ListaSitios:
		dist = menorDistancia((la,lon),Punto,distancia)
		if dist != None:
			PuntosCercanosList.append((dist,(Id,Tipo,Nombre,la,lon)))
	return PuntosCercanosList

def getPuntoMasCercano(Punto, distancia, ListaSitios):
	lista = getPuntosCercanos(Punto, distancia, ListaSitios)
	if len(lista) > 0:
		return min(lista)
	else:
		return (None,None)


Lista= [[1,"Biblioteca","Biblioteca1", 37.357924, -5.986320], [2,"Museo","Museo1",37.362922, -5.975878]]
PuntoA = (37.355508, -5.987698)
print(getPuntosCercanos(PuntoA,50,Lista))