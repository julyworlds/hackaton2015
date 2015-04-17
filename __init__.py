import BDFuntions as bd
import utilidades
from flask import Flask, render_template, jsonify

#500m
distancia = 500
app = Flask(__name__, template_folder=".")

@app.route("/prueba")
def prueba():
    listaPuntos = [(37.355508, -5.987698),(37.855508, -5.287698)]
    listaTipos = bd.getTiposSitio()
    #sitios de interes
    sitios = list()
    for punto in listaPuntos:
        for tipo in listaTipos:
            lista = bd.getSitios(tipo,punto,distancia)
            for sitio in lista:
                if len([x for x in sitios if x[0]==sitio[0]]) ==0:
                    sitios.append(sitio)
    rutas = bd.getRutasRadio(listaPuntos[0],listaPuntos[-1],distancia)
    #TODO mostrar los sitios
    return jsonify(sitios=sitios,rutas=rutas)

@app.route("/prueba2")
def prueba2():
    listaPuntos = [(37.355508, -5.987698),(37.855508, -5.287698)]
    listaTipos = bd.getTiposSitio()
    #sitios de interes
    sitios = list()
    for punto in listaPuntos:
        for tipo in listaTipos:
            lista = bd.getSitios(tipo,punto,distancia)
            for sitio in lista:
                if len([x for x in sitios if x[0]==sitio[0]]) ==0:
                    sitios.append(sitio)
    return jsonify(sitios=sitios)

@app.route("/")
def mapview():
    # creating a map in the view
    return render_template('templates/map.html')

@app.route("/iniciarRuta",methods=['POST'])
def iniciarRuta():
    listaPuntos = request.form['puntos']
    listaTipos = request.form['tipos']
    #sitios de interes
    sitios = list()
    for punto in listaPuntos:
        for tipo in listaTipos:
            lista = bd.getSitios(tipo,punto,distancia)
            for sitio in lista:
                if len([x for x in sitios if x[0]==sitio[0]]) ==0:
                    sitios.append(sitio)
    rutas = bd.getRutasRadio(listaPuntos[0],listaPuntos[-1],distancia)
    #TODO mostrar los sitios
    #return jsonify(sitios=sitios,rutas=rutas)


@app.route("/calculaRutaSevici", methods=['POST'])
def calculaRutaSevici():
    puntoInicio = request.form['puntoInicio']
    puntoFin = request.form['puntoFin']
    (dist1,sevici1) = bd.getSevici(puntoInicio,distancia)
    (dist2,sevici2) = bd.getSevici(puntoInicio,distancia)
    if sevici1 != sevici2 and sevici1 != None and sevici2 != None:
        distP = utilidades.getDistancia(puntoInicio,puntoFin)
        if distP > dist1 + utilidades.getDistancia((sevici1[2],sevici1[3]),(sevici2[2],sevici2[3])) + dist2:
            return flask.jsonify(puntoInicio=sevici1,puntoFin=sevici2)
    return flask.jsonify(puntoInicio=None,puntoFin=None)

@app.route("/crearRuta", methods=['POST'])
def crearRuta():
    listaPuntos = request.form['puntos']
    ruta = ""
    for ((puntox,puntoy),tipo, Id) in listaPuntos:
        ruta += Id+":"+tipo+","
    ruta = ruta[:-1]
    idruta = bd.createRuta(ruta, current_user.id)
    #going to show details
    detallesRuta = bd.getRutaById(idruta)
    

if __name__ == "__main__":
    app.run(debug=True)


