from pymongo import MongoClient
from libreria import Device

#info mongo client.
client= 'edison'
passdb = 'GnzNw2aAyJjKGOs7'
dbname = 'Iot_Devices'


#conection 
def get_db():
    try:
        url_client = MongoClient("mongodb+srv://"+client+":"+passdb+"@iotecuador.qbeh8.mongodb.net/"+dbname+"?retryWrites=true&w=majority")
        mydb = url_client.iotecuador
    except ConnectionError:
        print ("Error de coneccion con el servidor: --->"+client)
    return mydb     

#ingresar datos mongodb atlas

def insertar_devices(Device, band):
    if band == False:
        db = get_db()
        insertar = db.Devices.insert_one(Device.toCollection())
    else:
        print("La direccion IPV4 Ingresada ya existe")
    return insertar.inserted_id

Nombre = 'groupwork'
Direccion = '10.10.40.250'
Puerto = '22'
Estado = True

datos = Device(Nombre, Direccion, Puerto,Estado)


def find_devices(IPV4):
    db = get_db()
    band = False
    search = db.Devices.find({'Direccion':IPV4})
    for r in search:
        if(r != ''):
            print("contador search")
            print(r['Direccion'])#buscar por parametros
            print("La direccion IPV4 Ingresada ya existe", band)
            #print(r)todo
            band = True
        else:
            band = False
            print ("No existe la direccion IPV4 ingresada",band)    
    return band

exitIpv4 = find_devices(Direccion)
insertar_devices(datos, exitIpv4)

print ("find devices---->   " , exitIpv4)

id_registrosingresados = insertar_devices(datos,exitIpv4)
print ("se a ingresado exitosamente ID---->   ",id_registrosingresados)

input("Press enter to exit ;)")
