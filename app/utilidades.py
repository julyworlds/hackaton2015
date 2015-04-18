import math

def getDistancia(Punto1, Punto2):
	(x1,y1)= Punto1
	(x2,y2)= Punto2

	latitudDif= math.fabs(Punto2[0]-Punto1[0])
	longitudRadio = math.fabs(Punto2[1]-Punto1[1])

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

def getFirstLastSitio(listaRuta):
	first = None
	last = None
	for ele in listaRuta:
		splits = ele.split(":")
		Id = splits[0]
		tipo = Id = splits[1]
		if tipo != "Sevici":
			if first == None:
				first = Id
			last = Id
	return (first,last)

def listaPuntos(punto1, punto2, distancia):
	(x1,y1)= punto1
	(x2,y2)= punto2

	finalList = list()
	finalList.append(punto1)
	finalList.append(punto2)

	distanciaAux = distancia / 111100.
	latitudDif = x2-x1
	longitudRadio = y2-y1
	hip = math.sqrt(latitudDif**2 + longitudRadio**2)

	Aux1 = x1+(latitudDif/hip)*distanciaAux
	Aux2 = y1+(longitudRadio/hip)*distanciaAux
	check1 = math.fabs(latitudDif)/latitudDif
	check2 = math.fabs(longitudRadio)/longitudRadio
	while(x2*check1 > Aux1*check1 and y2*check2 > Aux2*check2):
		finalList.append((Aux1,Aux2))
		Aux1 += (latitudDif/hip)*distanciaAux
		Aux2 += (longitudRadio/hip)*distanciaAux
	
	return finalList

# Lista= [[1,"Biblioteca","Biblioteca1", 37.357924, -5.986320], [2,"Museo","Museo1",37.362922, -5.975878]]
# PuntoA = (37.355508, -5.987698)
# print(getPuntosCercanos(PuntoA,500,Lista))