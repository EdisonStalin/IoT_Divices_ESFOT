from pymongo import MongoClient
from libreria import divice

#info mongo client.
client= 'edison'
passdb = '1234567$'
dbname = 'iot_divice'

#conection 
def get_db():
    try:
        url_client = MongoClient("mongodb+srv://"+client+":"+passdb+"@cluster0.dxed2.mongodb.net/"+dbname+"?retryWrites=true&w=majority")
        mydb = url_client.iot_divice
    except ConnectionError:
        print ("Error de coneccion con el servidor"+client)
    return mydb     

#ingresar datos mongodb atlas

def insertar_divices(divice):
    db = get_db()
    insertar = db.divices.insert_one(divice.toCollection())
    return insertar.inserted_id

Nombre = 'groupwork'
Direccion = '10.10.40.00'
Puerto = '22'

datos = divice(Nombre, Direccion, Puerto)
insertar_divices(datos)

id_registrosingresados = insertar_divices(datos)
print ("se a ingresado exitosamente ID---->   ",id_registrosingresados)
input("Press enter to exit ;)")
