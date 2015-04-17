import math


		
def getPuntosCercanos(Punto,distancia, ListaSitios):
	(x,y) = Punto 

	PuntosCercanosList= list()
	
	for e in ListaSitios: 
		
		latitudRadio = e[3] - Punto[0]
		longitudRadio = e[4] - Punto[1]

		latitudMetros = (latitudRadio*111)*1000
		print("lat",latitudMetros)
		longtudMetris = (longitudRadio*111)*1000

		hip = math.sqrt( (latitudMetros)*(latitudMetros)+(longtudMetris)*(longtudMetris))
		hipKm =hip/1000
		print("hip",hipKm)
		if hipKm < distancia: 
			PuntosCercanosList.append(e)

	return PuntosCercanosList




# Lista= [[1,"Biblioteca","Biblioteca1", 37.357924, -5.986320], [2,"Museo","Museo1",37.362922, -5.975878]]
# PuntoA = (37.355508, -5.987698)
# print(getPuntosCercanos(PuntoA,1,Lista))