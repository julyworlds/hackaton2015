# -*- coding: utf-8 -*-
import sys
import sqlite3

def checkConnect():
    return sqlite3.connect('h4g.sqlite')

if len(sys.argv) != 2:
    print("introduce ruta fichero csv")
    sys.exit(0)


conexion = checkConnect()
cur = conexion.cursor()
fich = open(sys.argv[1],"r")


cur.execute("DELETE FROM Sitios")
for line in fich.readlines():
    (tipo,nombre,latitud,longitud) = line.split(",")
    if tipo != "Sevici" and tipo != "Policia":
        print(line.split(","))
        cur.execute("INSERT INTO Sitios (Tipo,Nombre,Latitud,Longitud) VALUES (?,?,?,?)",(tipo,nombre.decode("utf-8"),latitud,longitud))
conexion.commit()
cur.close()
conexion.close()

print("DONE")
