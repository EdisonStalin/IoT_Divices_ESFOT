from os import strerror
from re import T
from pymongo import MongoClient
import colorama
import pyfiglet
from libreria import Device
from bcolor import bcolors

#info mongo client.
client= 'edison'
passdb = 'GnzNw2aAyJjKGOs7'
dbname = 'Iot_Devices'

#conection MongoAtlas
def get_db():
    try:
        url_client = MongoClient("mongodb+srv://"+client+":"+passdb+"@iotecuador.qbeh8.mongodb.net/"+dbname+"?retryWrites=true&w=majority")
        mydb = url_client.iotecuador
    except ConnectionError:
        print ("Error de coneccion con el servidor: --->"+client)
    return mydb

#busqueda de la direcciones IP
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

import sys
try:
    import pygeoip #Para la geolcalización de las direcciones ip
except:
    print("Se debe instalar pygeoip para ejecutar este código. Ejecute pip install pygeoip.")
from ipaddress import IPv4Address #Manejos de IPv4
from random import randint #Para la generación de ips al azar
import socket #Manejo de sockets
from socket import close, socket, AF_INET, SOCK_STREAM, setdefaulttimeout,getfqdn #Comprobar sockets abiertos



def cabecera(): #Impresión de Texto Principal
    Title = pyfiglet.figlet_format("IOT ECUADOR") #install pip install pyfiglet
    Users = "Integrantes:"
    Integrates = "Edison Jumbo & Jefferson Llumiquinga"
    
    print (bcolors.HEADER + Title + bcolors.ENDC)
    print ((bcolors.WARNING+ Users+"\t" + bcolors.ENDC) + (bcolors.HEADER+ Integrates+"\n"+bcolors.ENDC ) )



#Direcciones IPV4  de Ecuador aleatorias. 

def generacion_IP_Ecuador():
    try:
        #ip = IPv4Address('{0}.{1}.{2}.{3}'.format(randint(0,255),randint(0,255),randint(0,255),randint(0,255)))
        ip = IPv4Address('181.39.210.85')
        obj = pygeoip.GeoIP('Geo/GeoLiteCity.dat')
        res = obj.record_by_addr(str(ip))
        if(ip.is_unspecified or ip.is_loopback or ip.is_multicast  or ip.is_reserved or ip.is_private or ip.is_link_local or obj.country_code_by_addr(str(ip))!="EC"):
            return generacion_IP_Ecuador()
        else:
            print("La ip ingresada es ", ip)
            for key,val in res.items():
                print('%s : %s' % (key, val))
        return str(ip)
    except Exception as e:
        print( bcolors.WARNING +"Se ha producido un error al crear una dirección Ipv4 randomica "+ip+bcolors.ENDC, e)
        exit(1)
        

#Recibe un host y los puertos que queremos comprobar y devuelve los puertos abiertos

def OpenPort(host, puerto):
    try:
        setdefaulttimeout(5)
        s=socket(AF_INET, SOCK_STREAM)
        resultado=s.connect_ex((str(host),puerto))
        if  resultado == 0:
            return True#puerto abierto
        else:
            return False#puerto cerrado     
        
    except Exception as e:
        print("Se ha producido un error al crear la  conexión desde el host "+host+" con el puerto:",puerto, "error: ", e)

## Funcion NoExisteIP
#Devuelve 0 si la IP no está en la base de datos
# Devuelve 1 si la IP existe pero hace más de un mes que se consultó
# Devuelve-1 si la IP existe y hace menos de un mes que se consultó
    
if __name__ == "__main__":
    colorama.init()
    cabecera()
    # Si se recibe un parámetro se comprobaran tantas direcciones ip como es parámetro (limitando a 1000)
    repeticiones=1#si usuario no ingresa ningun valor, por defecto es 100 direciones ip
    if len(sys.argv)==2:#tomamos el segundo valor de entrada despues del test,py numero
        try:
            repeticiones =int(sys.argv[1])#guardar en el valor de entrada en una variable.
        except :
            print("El uso del programa es sin parámtetros, con lo que se ejecutará 10 veces o aplicacion.py num, con lo que se ejecutará num veces siempre que sea menor o igual a 10")
            exit(-1)
        if int(repeticiones)>10:#maximo de direcciones IP 1000 a buscar.
            repeticiones=5
    print("Se van a examinar ",repeticiones, "direcciones IP localizadas en Ecuador")

    #Bucle repeticiones IP
    valor =0
    #PortsList=[161,8081,8182,8083,443,22,3001,1883,80,81,82,8008,8086,8080,9001,135,25,9000,21,23,53,264,8089,1723,8443,5001,445,9443] #juego reducido de puertos que se van a comprobar
    #PortsList=[22,23,25,53,80,81,82,433,554,1883,49152,1900,7000,5554,8080,8081,8008,5060,8883,5061,5150,5160,4550,5511,5550,6550,8866,56000,10000,10001]
    #PortsList=[5683, 5684,22,80,23,5060,8080,7547,8291,2323,81,25,2222,8081,9200,8090,52869,37777,37215,2332,2223,5061]
    PortsList=[22, 23, 25, 53, 80, 81, 110, 180, 443, 873, 2323, 5000, 5001, 5094, 5150, 5160, 7547, 8080, 8100, 8443, 8883, 49152, 52869, 56000,
    1728, 3001, 8008, 8009, 10001,223, 1080, 1935, 2332, 8888, 9100,2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007,21, 554, 888, 1159, 1160, 1161,
    1435, 1518, 3389, 4550, 5005, 5400, 5550, 6550, 7000, 8000, 8081, 8090, 8150, 8866, 9000, 9650, 9999, 10000, 18004, 25001, 30001, 34567, 37777,
    69, 135, 161, 162, 4786, 5431, 8291, 37215, 53413]

    for cont in range(0,repeticiones):
        ip=generacion_IP_Ecuador()#llamamos a la funcion, ip aleatorias
        print("IP generada:", ip)
        #Comprobamos si la IPv4 está en la base de datos MongpAtlas
        exist=find_devices(ip)
        active_port=False

        if(exist == False ):
            portOpen = []

            for port in PortsList:
                cont += 1
                open=OpenPort(ip,port)

                if open == True:
                    valor = (valor + 1)
                    print((bcolors.WARNING +"  "+ str(cont)+")  "+bcolors.ENDC)+(bcolors.OKGREEN+"PUERTO: "+ str(port)+"\t" +bcolors.ENDC)+(bcolors.OKGREEN+"Estado :"+str(open) +bcolors.ENDC))
                    portOpen.append(port)
                    active_port=True#Almenos 1 puerto activo.

                else:
                    print((bcolors.WARNING +"  "+ str(cont)+")  "+bcolors.ENDC)+(bcolors.FAIL+"PUERTO: "+ str(port)+"\t" +bcolors.ENDC)+(bcolors.FAIL+"Estado :"+str(open) +bcolors.ENDC))
                    active_port=False


    
    print("Puertos Activos",valor)
    print("Direccion Ipv4 --> "+ip+"  Puertos Abiertos--> ",portOpen)



    #resultado
    print("find devices---->   " , find_devices(ip))
    print(bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)
    input("Press enter to exit ;)")

