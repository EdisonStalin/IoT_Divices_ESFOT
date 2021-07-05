from os import strerror
from os import path #Para el path de la base de datos
import os
from re import T
from pymongo import MongoClient
import colorama
import pyfiglet
from bcolor import bcolors
from dns import resolver, reversename #Para los datos DNS
from datetime import datetime,timedelta #Para calcular la diferencia de fechas cuando la ip está en la bbdd
import time 
import socket #Manejo de sockets
from socket import socket, AF_INET, SOCK_STREAM, setdefaulttimeout,getfqdn #Comprobar sockets abiertos

from PIL import Image #imagenes

#clase atributos
from atributos import Device 

try:
    from selenium import webdriver #Abrir FireFox para capturas de pantallas
    import selenium #Para las capturas de las pantallas
except:
    print("Se debe instalar selenium para ejecutar este código. Ejecute pip install selenium.")
try:
    from ipwhois import IPWhois
except:
    print("Se debe instalar ipwhois para ejecutar este código. Ejecute pip install ipwhois.")


#info mongo client.
client= 'edison'
passdb = 'GnzNw2aAyJjKGOs7'
dbname = 'iotecuador'

#conection MongoAtlas
def get_db():
    try:
        url_client = MongoClient("mongodb+srv://"+client+":"+passdb+"@iotecuador.qbeh8.mongodb.net/"+dbname+"?retryWrites=true&w=majority")
        mydb = url_client.iotecuador
    except ConnectionError:
        print ("Error de coneccion con el servidor: --->"+client)
    return mydb

#busqueda de la direcciones IP


def find_devices(IPV4): #falta validar si pasa los 30 dias.
    db = get_db()#coneccion a la BD
    band = False
    search = db.Devices.find({'Direccion':IPV4})
    for r in search:
        if(r != ''):
            band = True
            print("contador search")
            print(r['Direccion'])#buscar por parametros
            print("La direccion IPV4 Ingresada ya existe", band)
            #print(r)todo
            
        else:
            band = False
            print ("No existe la direccion IPV4 ingresada",band)    
    return band

    #True (Mayor a 30 días)
    #False (Menor a 30 días)

def DateTime(IPV4):
    db = get_db()#coneccion a la BD
    resultado = False
    search = db.Devices.find({'Direccion':IPV4})
    for r in search:
        FechaBD = r['Fecha']#Fecha de la DB
        print('Fecha: ', FechaBD)
 
        if not FechaBD: #puede existir un valor null o vacio.
            return resultado

        cadena=datetime.strptime(FechaBD, "%Y-%m-%d %H:%M:%S")#Validad los paremetros de la fecha y hora
        ahora=datetime.now()#Obtener la hora actual de equipo
        treintadias = timedelta(days=30)
        fechaacomparar = ahora - treintadias
        print("Cadena:", cadena, "fechaacomparar:", fechaacomparar)

        if cadena<fechaacomparar: #tiene más de 30 días desde la ultima consulta
            resultado= True
        else:
            resultado= False
            print()

        print("Estado fecha", resultado)
        return resultado



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
    print ((bcolors.WARNING+ Users+"\t" + bcolors.ENDC) + (bcolors.HEADER+ Integrates+"\n"+bcolors.ENDC ))


def main():
    
    while True:
        print(bcolors.WARNING+"\n\nQué tipo de busqueda deseas realizar? \n"+bcolors.ENDC)

        print(bcolors.WARNING+" 1) "+bcolors.ENDC+bcolors.OKBLUE+" Busqueda aleatoria"+bcolors.ENDC)
        print(bcolors.WARNING+" 2) "+bcolors.ENDC+bcolors.OKBLUE+" Rango direcciones IPV4"+bcolors.ENDC)
        print(bcolors.WARNING+" 3) "+bcolors.ENDC+bcolors.OKBLUE+" Salir"+bcolors.ENDC)

        print("\n")

        num = input('Introduce el número: ')

        if num == str(1):
            print("1")
            break

        if num == str(2):
            print("2")
            break

        if num == str(3):
            print (bcolors.HEADER + "\n\n\t Gracias por usar el sistemas de Busqueda \n\n" + bcolors.ENDC)
            exist
            break

        if num == '':
            print('No has ingresado una opción ')
            print('Favor de volverlo a intentar.')

        else:
            print('La opcion ingresada no es la corecta')
            print('Favor de volverlo a intentar.')

    return num 

### Direcciones IPV4  de Ecuador aleatorias. 
def Generar_IP_Ecuador_Aleatoria():
    try:
        while True: #Bucle que se cierra una ves obtenga la direcciones ipv4 de Ecuador
            #ip = IPv4Address('{0}.{1}.{2}.{3}'.format(randint(0,255),randint(0,255),randint(0,255),randint(0,255)))
            ip = '186.5.59.70'
            obj = pygeoip.GeoIP('Geo/GeoLiteCity.dat')
            #res = obj.record_by_addr(str(ip))
            #if para validar que la direccion  ipv4 es de ecuador
            if(obj.country_code_by_addr(str(ip))=="EC"):
                print("La ip ingresada es ", ip)
                #for key,val in res.items():
                    #print('%s : %s' % (key, val))
                break

        return str(ip) #guardar ipv4 de Ecuador

    except Exception as e:
        print( bcolors.WARNING +"Se ha producido un error al crear una dirección Ipv4 randomica "+str(ip)+bcolors.ENDC, e)
        exit(1)
        
### Rango de direcciones Ipv4.



####################################################


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
        s.close()
        return resultado
    except Exception as e:
        print("Se ha producido un error al crear la  conexión desde el host "+host+" con el puerto:",puerto, "error: ", e)

##
# Captura la pantalla de la ip y el puerto dado
##
def capturadepantalla(ip, puerto):
    setdefaulttimeout(30)
    try:
        browser = webdriver.Firefox(
            executable_path=r'G:\IoT_Divices_ESFOT\FirefoxDriver\geckodriver.exe')
        browser.implicitly_wait(30) 
        browser.set_page_load_timeout(200)
        browser.get("http://{0}".format(ip)+":"+str(puerto))
        screenshot = browser.get_screenshot_as_png()
        state = True
        browser.quit()

        #guardamos el fichero en la carpeta capturas y almacenamos solo el nombre
        #componemos el nombre de fichero con la dirección IP, la hora, y la extensión PNG
        try:
            
            nombreimagen=ip+".png"
            print("1", nombreimagen)
            pathimagen=path.join(path.dirname(__file__),r"G:IoT_Divices_ESFOT/capturas/")
            print("2", pathimagen)
            img = Image.open(pathimagen+nombreimagen)#da error
            print("3", img)
            img.write(screenshot)
            print("4")
            img.close()    
            print("5")
        except Exception as e:
            print("Error al guardar imagen. Asegúrese de que el disco no está lleno. Error:", e)
            exit(1)
    
    except selenium.common.exceptions.WebDriverException as e:
        print("Se necesita FireFox para realizar una captura de pantalla. Error: ",e)
        exit(1)

    except Exception as e:
        state = False
        print("Hubo un error al capturar la imagen del navegador FireFox Mozilla: {0}".format(e))
        browser.quit()
  

    if state:
        return nombreimagen
    else:
        return None 
      

# Obtiene la información correspondiente a esos puertos y añadirlos o actualizarlos.
#####
#### 
###  
def addNewDevices(ip, portOpen, exist, fecha):

   
            
    for puerto in portOpen:
        try:
            connection = socket(AF_INET, SOCK_STREAM)
            connection.connect((ip, puerto))
            connection.send(b'HEAD / HTTP/1.0\r\n\r\n')
            banner=""#Inicializamos banner por si al final hay error en el siguiente paso
            banner = connection.recv(1024)
            aux = str(banner).replace('\\r\\n','<br/>')
            banner = aux[2:len(aux)-3] #Quitamos el espacio incial y los finales que no interesan. Ya tenemos el banner
                
        except Exception as e:
            print("Error al realizar la conexión con el banner:", e)
        connection.close()

        #adñadir información de la direccion Ipv4
        obj = pygeoip.GeoIP('Geo/GeoLiteCity.dat')
        location = obj.record_by_addr(str(ip))
            #for key,val in res.items():
                #print('%s : %s' % (key, val))


        dominio=getfqdn(ip) ##Aquí tenemos el nombre de dominio de la ip
        whois=IPWhois(ip).lookup_whois() #Obtenemos la información del whois
        dns=reversename.from_address(ip)
        datosdns=str(dns)
        date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    
        #if puerto==80 or puerto==8080 or puerto ==8081:
            #imagen= capturadepantalla(ip, puerto)
            #print("realiza captura en los puertos 80, 8080 & 8081")  
        #else:
            #imagen="Noimagen.png"
        #Almacenamos información
        print("Banner:", banner)
        print("NombredeDominio:", dominio)
        print("Datos Whois:", whois)
        print("DNS:", datosdns)
        print("Fecha:", date)
        
        #Almacenar en una arreglo la información del puerto.
        puerto = {'Puerto' : str(puerto), 'Banner' : str(banner)}



        if exist == False:#agregar la infromacion a la data por primera vez.

            db = get_db()#Conexion bd mongoatlas.
            # Atributos de la clase Devices (ip, fecha ,location, whois, dominio, dns, puerto)
            datos = Device(str(ip), str(date), location, whois, str(dominio), str(dns), puerto)
            db.Devices.insert_one(datos.toCollection())
             

        if fecha == True:#fecha paso los 30 días, solo se debe realizar una actualizacion
            db = get_db()
            db.Devices.update_one({"Direccion":str(ip)},{"$set":{"Fecha": str(date), "puerto": puerto}})
            




#finalización de la busqueda
def new_search(valor):
    if ((valor == "Si") or (valor == "si")):
        return main()
    else:
        print (bcolors.HEADER + "\n\n\t Gracias por usar el sistemas de Busqueda \n\n" + bcolors.ENDC)
        exist



if __name__ == "__main__":
    colorama.init()
    cabecera()
    ipv4 = main()

    

    # Si se recibe un parámetro se comprobaran tantas direcciones ip como es parámetro (limitando a 1000)
    repeticiones=1#si usuario no ingresa ningun valor, por defecto es 100 direciones ip
    if len(sys.argv)==2:#tomamos el segundo valor de entrada despues del test,py numero
        try:
            repeticiones =int(sys.argv[1])#guardar en el valor de entrada en una variable.
        except:
            print("El uso del programa es sin parámtetros, con lo que se ejecutará 10 veces o aplicacion.py num, con lo que se ejecutará num veces siempre que sea menor o igual a 10")
            exit(-1)
        if int(repeticiones)>10:#maximo de direcciones IP 1000 a buscar.
            repeticiones=100
    print("Se van a examinar ",repeticiones, "direcciones IP localizadas en Ecuador")

    #Bucle repeticiones IP
    valor =0
    #PortsList=[80]
    #PortsList=[161,8081,8182,8083,443,22,3001,1883,80,81,82] #juego reducido de puertos que se van a comprobar
    PortsList=[21,443]
    #PortsList=[5683, 5684,22,23,5060,8080,7547,8291,2323,25,2222,9200,8090,52869,37777,37215,2332,2223,5061]
    #PortsList=[22, 23, 25, 53, 80, 81, 110, 180, 443, 873, 2323, 5000, 5001, 5094, 5150, 5160, 7547, 8080, 8100, 8443, 8883, 49152, 52869, 56000,
    #1728, 3001, 8008, 8009, 10001,223, 1080, 1935, 2332, 8888, 9100,2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007,21, 554, 888, 1159, 1160, 1161,
    #1435, 1518, 3389, 4550, 5005, 5400, 5550, 6550, 7000, 8000, 8081, 8090, 8150, 8866, 9000, 9650, 9999, 10000, 18004, 25001, 30001, 34567, 37777,
    #69, 135, 161, 162, 4786, 5431, 8291, 37215, 53413]

    
    valor = 0


    #agregarle en una funcion 
    for cont in range(0,repeticiones):
        #validar el tipo de busqueda.
        if ipv4 == str(1):
            ip=Generar_IP_Ecuador_Aleatoria()#llamamos a la funcion, ip aleatorias
        if ipv4 == str(2):
            ip='93.40.9.92'
        print("IP generada:", ip)
        #Comprobamos si la IPv4 está en la base de datos MongpAtlas
        exist=find_devices(ip)#True (IPV4 ya exite ) / False (Ipv4 no exite)
        fecha = DateTime(ip)#True (Mayor a 30 días) / False (Menor a 30 días)
        print("Exit, estado: ", exist)

        if(exist == False or fecha == True ):#la ipv4 no exite / tiempo mayor a 30 dias
            portOpen = []

            for port in PortsList:
                #cont += 1
                open=OpenPort(ip,port)

                if  open:
                    valor = (valor + 1)
                    #print((bcolors.WARNING +"  "+ str(cont)+")  "+bcolors.ENDC)+(bcolors.OKGREEN+"PUERTO: "+ str(port)+"\t" +bcolors.ENDC)+(bcolors.OKGREEN+"Estado :"+str(open) +bcolors.ENDC))
                    portOpen.append(port)

            addNewDevices(ip, portOpen, exist, fecha)
                    
                #else:
                    #print((bcolors.WARNING +"  "+ str(cont)+")  "+bcolors.ENDC)+(bcolors.FAIL+"PUERTO: "+ str(port)+"\t" +bcolors.ENDC)+(bcolors.FAIL+"Estado :"+str(open) +bcolors.ENDC))
        
        else:
            print("La dirección IPv4", ip , " ya existe" )

            


    print("Puertos Activos",valor)
    print("Direccion Ipv4 --> "+ip+"  Puertos Abiertos--> ",portOpen)
    
    #resultado
    print("find devices---->   " , find_devices(ip))
    
    print(bcolors.WARNING+"\n\nBusqueda Finalizada :) \n\n"+bcolors.ENDC)
    
    print(bcolors.WARNING+"Desea realizar una nueva busqueda \n"+bcolors.ENDC)
    valor = input("Ingrese Si o No: ")
    new_search(valor)




