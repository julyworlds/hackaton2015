import sys
import json
import sqlite3

def checkConnect():
    conexion = sqlite3.connect('h4g.sqlite')
    return conexion

if len(sys.argv) != 2:
    print("introduce ruta fichero csv")
    sys.exit(0)

    
conexion = checkConnect()
cur = conexion.cursor()
fich = open(sys.argv[1],"r")
data = json.loads(fich.read())

cur.execute("DELETE FROM Sevici")

for line in data["network"]["stations"]:
    nombre = line["name"]
    latitud = line["latitude"]
    longitud = line["longitude"]
    cur.execute("INSERT INTO Sevici (Nombre,Latitud,Longitud) VALUES (?,?,?)",(nombre,latitud,longitud))
conexion.commit()
cur.close();conexion.close()
conexion.close()

print("DONE")
