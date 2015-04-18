from flask import Flask, jsonify, render_template, request, flash, redirect, url_for, g
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from flask.ext.sqlalchemy import SQLAlchemy
from uuid import uuid4
import BDFuntions as bd
import json

# Inicia la aplicacion
#500m
distancia = 500
app = Flask(__name__, template_folder="templates")
unicode = str

# Inicia el login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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

# Configura la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///h4g.sqlite'
db = SQLAlchemy(app)


class User(db.Model):
    " Clase que modela al usuario "
    __tablename__ = "Usuarios"
    id = db.Column('ID',db.Integer , primary_key=True)
    username = db.Column('Usuario', db.String(20), unique=True , index=True)
    password = db.Column('Password' , db.String(10))
    email = db.Column('Correo',db.String(50),unique=True , index=True)
 
    def __init__(self , username ,password , email):
        self.username = username
        self.password = password
        self.email = email

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return '<User %r>' % (self.username)


@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['username'] , request.form['password'],request.form['email'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))
 
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index')) 

@app.before_request
def before_request():
    g.user = current_user

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/")
def index():
    # creating a map in the view
    return render_template('index.html')

@app.route("/mapa")
def showMap():
    return render_template("map.html",tipos=bd.getTiposSitio())

@app.route("/iniciarRuta",methods=['POST'])
def iniciarRuta():
    listaPuntos = json.loads(request.form['puntos'])
    #listaTipos = json.dumps(request.form['tipos'])
    listaTipos = bd.getTiposSitio()
    #sitios de interes
    sitios = list()
    for punto in listaPuntos:
        punto = tuple(punto)
        for tipo in listaTipos:
            lista = bd.getSitios(tipo,punto,distancia)
            for sitio in lista:
                if len([x for x in sitios if x[0]==sitio[0]]) ==0:
                    sitios.append(sitio)
    rutas = bd.getRutasRadio(listaPuntos[0],listaPuntos[-1],distancia)
    #TODO mostrar RUTAS semejantes
    return render_template("map2.html", puntos=sitios, tipos=listaTipos, rutas=rutas)

@app.route("/calculaRutaSevici", methods=['POST'])
def calculaRutaSevici():
    puntoInicio = request.form['puntoInicio']
    puntoFin = request.form['puntoFin']
    (dist1,sevici1) = bd.getSevici(puntoInicio,distancia)
    (dist2,sevici2) = bd.getSevici(puntoInicio,distancia)
    if sevici1 != sevici2 and sevici1 != None and sevici2 != None:
        distP = utilidades.getDistancia(puntoInicio,puntoFin)
        if distP > dist1 + utilidades.getDistancia((sevici1[2],sevici1[3]),(sevici2[2],sevici2[3])) + dist2:
            return jsonify(puntoInicio=sevici1,puntoFin=sevici2)
    return jsonify(puntoInicio=None,puntoFin=None)

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

@app.route("/detallesRuta", methods=['GET'])    
def detallesRuta():
    idRuta = request.form['idRuta']
    detallesRuta = bd.getRutaById(idruta)



if __name__ == "__main__":
    app.secret_key = '1098247ijdhasf0982134jkb9812351'
    app.run(debug=True)
