from warnings import resetwarnings
from dns.rdatatype import NULL
from pymongo import MongoClient ## conexión a la base de datos
import sys
import colorama ## Imprime texto en colores
import pyfiglet ## Modificar la forma del Título
from dns import reversename ## Para obtener el DNS
from datetime import datetime,timedelta ## Para calcular la diferencia de fechas cuando la ip está en la BD
from socket import socket, AF_INET, SOCK_STREAM, setdefaulttimeout,getfqdn ## Comprobar sockets abiertos
from selenium import webdriver ## Abrir FireFox para capturas de pantallas
import selenium ## Para las capturas de las pantallas
from ipwhois import IPWhois ## Whois
import pygeoip ##Para la geolcalización de las direcciones ip
from ipaddress import IPv4Address #Manejos de IPv4
from random import randint #Para la generación de ipv4 al azar


## Clase atributos
from atributos import Device
## Clase contenedora de los colores.
from bcolor import bcolors 

## Información del client de la base de datos.
client= 'edison'
passdb = 'GnzNw2aAyJjKGOs7'
dbname = 'iotecuador'

## Conexión MongoAtlas
def get_db():
    try:
        url_client = MongoClient("mongodb+srv://"+client+":"+passdb+"@iotecuador.qbeh8.mongodb.net/"+dbname+"?retryWrites=true&w=majority")
        mydb = url_client.iotecuador
    except ConnectionError:
        print ("Error de coneccion con el servidor: --->"+client)
    return mydb



## Valida la existencia de la Ipv4 en la BD
def find_devices(IPV4):
    db = get_db()# Conexiíon a la BD
    band = False
    search = db.Devices.find({'Direccion':IPV4})

    for r in search:
        if(r != ''):
            band = True ## Existe!
            #print("La direccion IPV4 Ingresada ya existe", band)
            #print(r['Direccion'])#buscar por parametros
            #print(r)todo 
        else:
            band = False ## No Existe!
            #print ("No existe la direccion IPV4 ingresada",band)    
    return band

    
## Valida la fecha que se agregó la Ipv4 en la BD
##True (Mayor a 30 días)
##False (Menor a 30 días)

def DateTime(IPV4):
    db = get_db()# Conexiíon a la BD
    resultado = False
    search = db.Devices.find({'Direccion':IPV4})

    for r in search:
        FechaBD = r['Fecha']
        print('Fecha que se agrego a la BD: ', FechaBD)
 
        if not FechaBD: #puede existir un valor null o vacio.
            return resultado

        cadena=datetime.strptime(FechaBD, "%Y-%m-%d %H:%M:%S")## Válida los paremetros de la fecha y hora
        ahora=datetime.now()## Obtener la hora actual de equipo
        treintadias = timedelta(days=30)
        fechaacomparar = ahora - treintadias
        #print("Cadena:", cadena, "fecha a comparar:", fechaacomparar)

        if cadena<fechaacomparar: ## Tiene más de 30 días desde la última consulta
            resultado= True
        else:
            resultado= False
            print()

        #print("Estado fecha", resultado)
        return resultado







def cabecera(): #Impresión de Texto Principal
    Title = pyfiglet.figlet_format("IOT ECUADOR") #install pip install pyfiglet
    Users = "Integrantes:"
    Integrates = "Edison Jumbo & Jefferson Llumiquinga"
    
    print (bcolors.HEADER + Title + bcolors.ENDC)
    print ((bcolors.WARNING+ Users+"\t" + bcolors.ENDC) + (bcolors.HEADER+ Integrates+"\n"+bcolors.ENDC ))




def main():
    
    while True:
        print(bcolors.WARNING+"\n\nQué deseas Hacer.? \n"+bcolors.ENDC)

        print(bcolors.WARNING+" 1) "+bcolors.ENDC+bcolors.OKBLUE+" Recolectar datos de direcciones Ipv4"+bcolors.ENDC)
        print(bcolors.WARNING+" 2) "+bcolors.ENDC+bcolors.OKBLUE+" Salir"+bcolors.ENDC)
        print("\n")

        num = input('Introduce el Opción: ')

        if num == str(1):
            print("\n")
            print(bcolors.OKBLUE+" Cúantas direcciones Ipv4 Aleatorias deseas: "+bcolors.ENDC)
            repeticiones = input('Introduce la cantidad: ')
            cant =  repetir(repeticiones)
            agregar(cant)
            break


        if num == str(2):
            print (bcolors.HEADER + "\n\n\t Gracias por usar el sistemas de Busqueda \n\n" + bcolors.ENDC)
            exit(1)
            

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
            
            ip = '190.15.136.171'
            #ip = '200.7.195.124' ## Conexión fallida
            #ip = '200.1.112.207' ## No se encuentra activa
            obj = pygeoip.GeoIP('Geo/GeoLiteCity.dat')
            res = obj.record_by_addr(str(ip))
            ## Validar que la direccion  ipv4 es de ecuador
            if(obj.country_code_by_addr(str(ip))=="EC"):
                #print("La ip ingresada es ", ip)
                for key,val in res.items():
                    print('%s : %s' % (key, val))
                break
            #else:
                #print('la dirrección Ipv4: '+ str(ip) + ', esta inactiva')
                #exit(1)
            
        return str(ip) #guardar ipv4 de Ecuador

    except Exception as e:
        print( bcolors.WARNING +"Se ha producido un error al crear una dirección Ipv4 randomica "+str(ip)+bcolors.ENDC, e)
        exit(1)
        
### Rango de direcciones Ipv4.



####################################################


#Recibe un host y los puertos que queremos comprobar y devuelve los puertos abiertos
def OpenPort(host, puerto):
    try:
        setdefaulttimeout(5) ## Tiempo de conexión
        s=socket(AF_INET, SOCK_STREAM)
        resultado=s.connect_ex((str(host),puerto))
        if  resultado == 0:
            return True ## Puerto abierto
        else:
            return False ## Puerto cerrado     
        s.close()
        return resultado
    except Exception as e:
        print("Se ha producido un error al crear la  conexión desde el host "+host+" con el puerto:",puerto, "error: ", e)


## Captura la pantalla de la ip y el puerto dado
## Al existir una imagen con el mismo nombre, simplemente lo actualiza.
## En caso que la ruta del directorio contenedor de sea incorrecta, se envia un mensaje con el recpectivo error!
## El nombre que toma la img es la dirección Ipv4.

def capturadepantalla(ip, puerto):
    setdefaulttimeout(30)
    try:
        browser = webdriver.Firefox(executable_path=r'G:\\IoT_Divices_ESFOT\\FirefoxDriver\\geckodriver.exe')
        browser.implicitly_wait(30) 
        browser.set_page_load_timeout(200)
        browser.get("http://{0}".format(ip)+":"+str(puerto))
        nombreimagen=str(ip)+".png" ## Nombre de la Img.
        screenshot = browser.get_screenshot_as_file(r"G:\\IoT_Divices_ESFOT\\capturas\\"+ str(nombreimagen)) ##Bool
        #print("variable bool",screenshot)
        state = screenshot
        browser.quit()
    
    except selenium.common.exceptions.WebDriverException as e:
        print("Se necesita FireFox para realizar una captura de pantalla. Error: ",e)
        exit(1)

    except Exception as e:
        state = False
        print("Hubo un error al capturar la imagen del navegador FireFox Mozilla: {0}".format(e))
        browser.quit()
        exit(1)

    if state:
        return nombreimagen
    else:
        return None 
      

# Obtiene la información correspondiente a esos puertos y añadirlos o actualizarlos.
#####
#### 
###  
def addNewDevices(ip, portOpen, exist, fecha):

    puertoList =[]

    for puerto in portOpen:
        try:
            connection = socket(AF_INET, SOCK_STREAM)
            connection.connect((ip, puerto))
            connection.send(b'HEAD / HTTP/1.0\r\n\r\n')
            banner=""## Inicializamos banner por si al final hay error en el siguiente paso
            banner = connection.recv(1024)
            aux = str(banner).replace('\\r\\n','<br/>')
            banner = aux[2:len(aux)-3] ## Quitamos el espacio incial y los finales que no interesan. Ya tenemos el banner
                
        except Exception as e:
            print("Error al realizar la conexión con el banner:", e)
        connection.close()

        #adñadir información de la direccion Ipv4
        obj = pygeoip.GeoIP('Geo/GeoLiteCity.dat')
        location = obj.record_by_addr(str(ip))
        #print('location: ', location)
        #for key,val in location.items():
            #print('%s : %s' % (key, val))
        
        if puerto==80 or puerto==8080 or puerto ==8081:
            imagen=capturadepantalla(ip, puerto)
            print("Se a realizado exitosamente la catura.")  
        else:
            imagen="Noimagen.png"

        
            
        ## Almacena 'Documentos' dentro de un arreglo, usando append.
        puerto ={'Puerto' : str(puerto), 'Banner' : str(banner)}
        puertoList.append(puerto)  

    ## Información de los puertos:
    dominio=getfqdn(ip) ## Dominio
    whois=IPWhois(ip).lookup_whois() ## Whois
    dns=reversename.from_address(ip) ## DNS
    date=datetime.now().strftime('%Y-%m-%d %H:%M:%S') ## Fecha y hora del Equipo.



    #print("Banner:", banner)
    #print("NombredeDominio:", dominio)
    #print("Datos Whois:", whois)
    #print('Datos Dns', dns)
    #print("Fecha:", date)
    #print("puertos", puertoList) 


    ## Agrega la infromacion a la base de datos por primera vez.
    ## Los atributos que se asignan son los siguientes: (ip, img, fecha ,location, whois, dominio, dns, puerto)
    if exist == False: 

        db = get_db()
        datos = Device(str(ip), str(imagen), str(date), location, whois, str(dominio), str(dns), puertoList)
        db.Devices.insert_one(datos.toCollection())

    #La fecha paso los 30 días, solo se debe realizar una actualización, (Fecha: )       
    if fecha == True:

        db = get_db()
        db.Devices.update_one({"Direccion":str(ip)},{"$set":{"Fecha": str(date), "puerto": puertoList}})
            

#finalización de la busqueda
def new_search(valor):
    if ((valor == "Si") or (valor == "si") or (valor == "s") or (valor == "S")):
        return main()
    else:
        print (bcolors.HEADER + "\n\n\t Gracias por usar el sistemas de Busqueda \n\n" + bcolors.ENDC)
        exit(1)

    # Si se recibe un parámetro se comprobaran tantas direcciones ip como es parámetro (limitando a 1000)

def repetir(repeticiones):
    #repeticiones=1 ## si usuario no ingresa ningun valor, por defecto es 1 direción ip
    if int(repeticiones) > 1000:   ## Realizara una busqueda de 100 direciones ipv4.
        repeticiones = 100
    
    print("Se van a examinar ",repeticiones, "direcciones IP localizadas en Ecuador")
    return repeticiones

def agregar(repeticiones):
    #Bucle repeticiones IP
    valor =0
    #PortsList=[80]
    #PortsList=[161,8081,8182,8083,443,22,3001,1883,80,81,82] #juego reducido de puertos que se van a comprobar
    #PortsList=[80]
    #PortsList=[5683, 5684,22,23,5060,8080,7547,8291,2323,25,2222,9200,8090,52869,37777,37215,2332,2223,5061]
    PortsList=[22, 23, 25, 53, 80, 81, 110, 180, 443, 873, 2323, 5000, 5001, 5094, 5150, 5160, 7547, 8080, 8100, 8443, 8883, 49152, 52869, 56000,
    1728, 3001, 8008, 8009, 10001,223, 1080, 1935, 2332, 8888, 9100,2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007,21, 554, 888, 1159, 1160, 1161,
    1435, 1518, 3389, 4550, 5005, 5400, 5550, 6550, 7000, 8000, 8081, 8090, 8150, 8866, 9000, 9650, 9999, 10000, 18004, 25001, 30001, 34567, 37777,
    69, 135, 161, 162, 4786, 5431, 8291, 37215, 53413]  
    
    #agregarle en una funcion 
    #print("repeticiones", repeticiones)
    for cont in range(0, int(repeticiones)):
        #validar el tipo de busqueda.
        ip=Generar_IP_Ecuador_Aleatoria()   ## llamamos a la funcion, ip aleatorias
        print("IP generada:", ip)
        #Comprobamos si la IPv4 está en la base de datos MongpAtlas
        exist=find_devices(ip)#True (IPV4 ya exite ) / False (Ipv4 no exite)
        fecha = DateTime(ip)#True (Mayor a 30 días) / False (Menor a 30 días)
        #print("Exit, estado: ", exist)

        if(exist == False or fecha == True):#la ipv4 no exite / tiempo mayor a 30 dias
            portOpen = []
            validar = portOpen.__len__
            print

            for port in PortsList:
                cont += 1
                open=OpenPort(ip,port)

                if  open == True:
                    valor = (valor + 1)
                    print((bcolors.WARNING +"  "+ str(cont)+")  "+bcolors.ENDC)+(bcolors.OKGREEN+"PUERTO: "+ str(port)+"\t" +bcolors.ENDC)+(bcolors.OKGREEN+"Estado :"+str(open) +bcolors.ENDC))
                    portOpen.append(port)
                else:
                    print((bcolors.WARNING +"  "+ str(cont)+")  "+bcolors.ENDC)+(bcolors.FAIL+"PUERTO: "+ str(port)+"\t" +bcolors.ENDC)+(bcolors.FAIL+"Estado :"+str(open) +bcolors.ENDC))
            validar = len(portOpen)
            print("contar ", validar)

            if int(validar) != 0:
                addNewDevices(ip, portOpen, exist, fecha)
                print("Direccion Ipv4 --> "+ip+"  Puertos Abiertos--> ",portOpen)        
            else:
                print("La dirección Ipv4,"+ ip +" No contiene ningun puerto activo")

        else:
            print("La dirección IPv4", ip , " ya existe y es menor a 30 días")

    print(bcolors.WARNING+"\n\nBusqueda Finalizada :) \n\n"+bcolors.ENDC)
            

    #resultado
def final():    
    
    print(bcolors.WARNING+"Desea realizar una nueva busqueda \n"+bcolors.ENDC)
    valor = input("Ingrese Si o No: ")
    new_search(valor)





    

if __name__ == "__main__":
    colorama.init()
    cabecera()
    main()
    final()
    






