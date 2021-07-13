from warnings import resetwarnings
from dns.rdatatype import NULL
from pymongo import MongoClient ## conexión a la base de datos
import sys
import time
import colorama ## Imprime texto en colores
import pyfiglet ## Modificar la forma del Título
from dns import reversename ## Para obtener el DNS
from datetime import datetime,timedelta ## Para calcular la diferencia de fechas cuando la ip está en la BD
from socket import socket, AF_INET, SOCK_STREAM, setdefaulttimeout,getfqdn ## Comprobar sockets abiertos
from selenium import webdriver ## Abrir FireFox para capturas de pantallas
import selenium ## Para las capturas de las pantallas
from ipwhois import IPWhois ## Whois
import pygeoip ##Para la geolcalización de las direcciones ip
from ipaddress import IPv4Address, ip_address #Manejos de IPv4
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
##True: Existe la IPv4 con estado True  (Puertos Abiertos)
##False: La IPv4 no existe ó existe pero con estado False  (Puertos Cerrados)

def find_devices(IPV4):
    db = get_db()# Conexiíon a la BD
    valor = 0
    search = db.Devices.find({'Direccion':IPV4})
    for r in search:
        Ipv4Bd = r['Direccion']
        print('Ipv4Bd',Ipv4Bd)
        estadoBd = r['Estado']
        print('estadoBd',estadoBd)
        fechaBd = r['Fecha']
        print('fechaBd',fechaBd)
        
    if(Ipv4Bd != ''):## Existe! 

        if(estadoBd == True): ##Existen Puertos Abiertos  
            print('Ingreso al estado True')
            Tiempoconsulta = 30 ##Tiempo en días.

            valor = DateTime(fechaBd, Tiempoconsulta)
            print('valor',valor)
            
        else:
            print('Ingreso al estado False')
            Tiempoconsulta = 15 ##Tiempo en días.

            valor = DateTime(fechaBd,Tiempoconsulta)
            print('valor',valor)

            #print("La direccion IPV4 Ingresada ya existe", band)
            #print(r['Direccion'])#buscar por parametros
            #print(r)todo 
        
    else:## No Existe!
        valor = 0 
        #print ("No existe la direccion IPV4 ingresada",band)
            
    return valor


def DateTime(FechaBD, days):#Fecha de la Base de datos
        cadena=datetime.strptime(FechaBD, "%Y-%m-%d %H:%M:%S")## Válida los paremetros de la fecha y hora
        ahora=datetime.now()## Obtener la hora actual de equipo
        treintadias = timedelta(days=days)## Establecer los días máximos a superar.
        fechaacomparar = ahora - treintadias
        #print("Cadena:", cadena, "fecha a comparar:", fechaacomparar)

        if cadena<fechaacomparar: ## Supera el limite de días establecidos.
            resultado= 1
        else:
            resultado= -1
            print()

        #print("Estado fecha", resultado)
        return resultado    


if __name__ == "__main__":
    ip = "186.66.117.45"
    find_devices(ip)