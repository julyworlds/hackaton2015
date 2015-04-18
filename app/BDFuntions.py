import sqlite3
import utilidades

def checkConnect():
    return sqlite3.connect('h4g.sqlite')

#Usuarios
def register(username,password,mail):
    conexion = checkConnect();cur = conexion.cursor()
    cur.execute("SELECT * from Usuarios Where Usuario=? or Correo=?",(username,mail))
    res = cur.fetchone()
    if res == None:
        return False
    cur.execute("INSERT INTO Usuarios (Usuario,Password,Correo) VALUES (?,?,?)", (username,password,mail))
    conexion.commit()
    cur.close();conexion.close()
    return True

def login(username,password):
    conexion = checkConnect();cur = conexion.cursor()
    cur.execute("SELECT  * from Usuarios Where Usuario=?",(username,))
    res = cur.fetchone()
    if res == None:
        return False
    cur.close();conexion.close()
    return res[2] == password

#Sitios
def getSitios(tipo=None, punto=None, distancia=None):
    conexion = checkConnect();cur = conexion.cursor()
    sql = "SELECT * from Sitios "
    if tipo != None:
        sql += "Where Tipo=? "
        cur.execute(sql,(tipo,))
    else:
        cur.execute(sql)
    res = cur.fetchall()
    cur.close();conexion.close()
    if punto != None and distancia != None:
        return [ x[1] for x in utilidades.getPuntosCercanos(punto,distancia,res)]
    else:
        return res

def getTiposSitio():
    conexion = checkConnect();cur = conexion.cursor()
    sql = "SELECT DISTINCT Tipo from Sitios "
    cur.execute(sql)
    res = cur.fetchall()
    cur.close();conexion.close()
    return [x[0] for x in res]    

def getSitioById(Id):
    conexion = checkConnect();cur = conexion.cursor()
    sql = "SELECT * from Sitios Where ID=?"
    cur.execute(sql,(Id))
    res = cur.fetchone()
    cur.close();conexion.close()
    return res

#Sevici
def getSevici(punto=None, distancia=None):
    conexion = checkConnect();cur = conexion.cursor()
    sql = "SELECT * from Sevici "
    cur.execute(sql)
    res = cur.fetchall()
    cur.close();conexion.close()
    res2 = [(x[0],"Sevici",x[1],x[2],x[3]) for x in res]
    if punto != None and distancia != None:
        return utilidades.getPuntoMasCercano(punto,distancia,res2)
    else:
        return res

#Rutas
def createRuta(Ruta, IDusuario):
    conexion = checkConnect();cur = conexion.cursor()
    cur.execute("INSERT INTO Rutas (Ruta,IDUsuario) VALUES (?,?)", (Ruta,IDusuario))
    conexion.commit()
    res = cur.lastrowid
    cur.close();conexion.close()
    return res

def getRutaById(Id):
    conexion = checkConnect();cur = conexion.cursor()
    sql = "SELECT Rutas.ID,Rutas.Ruta,ValoracionRutas.Comentarios,ValoracionRutas.Tiempo,ValoracionRutas.Valoracion,Usuarios.Usuario from Rutas JOIN ValoracionRutas ON Rutas.ID=ValoracionRutas.IDRuta JOIN Usuarios ON ValoracionRutas.IDUsuario=Usuarios.ID Where Rutas.ID=?"
    cur.execute(sql,(Id,))
    res = cur.fetchall()
    cur.close();conexion.close()
    toRet = (res[0][0],res[0][1],[(x[2],x[3],x[4],x[5]) for x in res])
    return res

def getRutasRadio(puntoInicio, puntoFin, distancia):
    conexion = checkConnect();cur = conexion.cursor()
    sql = "SELECT * from Rutas"
    cur.execute(sql)
    res = cur.fetchall()
    cur.close();conexion.close()
    res = []
    for (Id,Ruta,IDUsuario) in res:
        sitios = Ruta.split(",")
        (firstId,lastId) = utilidades.getFirstLastSitio(sitios)
        if firstId != None and lastId != None:
            first = getSitioById(firstId)
            last = getSitioById(lastId)
            if utilidades.menorDistancia((first[3],first[4]),puntoInicio,distancia) and utilidades.menorDistancia((last[3],last[4]),puntoFin,distancia):
                res.append(Id)
    return [getRutaById(x) for x in res]

#ValoracionRutas
def createValoracionRutas(comentarios, tiempo, valoracion, idUsuario, idRuta):
    conexion = checkConnect();cur = conexion.cursor()
    cur.execute("INSERT INTO ValoracionRutas (Comentarios, Tiempo, Valoracion, IDUsuario, IDRuta) VALUES (?,?,?,?,?)", (comentarios,tiempo,valoracion,idUsuario,idRuta))
    conexion.commit()
    cur.close();conexion.close()

def existeValoracionRuta(idRuta, idUsuario):
    conexion = checkConnect();cur = conexion.cursor()
    cur.execute("SELECT * FROM ValoracionRutas Where IDRuta=? and IDUsuario=?", (idRuta,idUsuario))
    row = cur.fetchone()
    cur.close();conexion.close()
    return row != None
    