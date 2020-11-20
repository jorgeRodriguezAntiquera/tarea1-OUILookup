#!/usr/bin/env python

# Modo de uso:
#
# Uso: ./OUILookup.py --ip <ip> | --mac <mac> [--help] 
#
# Parametros:
#     --ip: specify the IP of the host to query.
#	  --mac: specify the MAC address to query. p.e. aa:bb:cc:00:00:00.
#     --help: show this message and quit.
     

import getopt
import sys
import re
import requests
import socket
from uuid import getnode as get_mac
#Cuerpo principal
def main():
    try:
        #para tener opciones largas, es necesario colocar las opciones cortas respectivas,
        #aunque no se utilicen. En este caso: -r y -m
        options, args = getopt.getopt(sys.argv[1:],"r,m",['ip=','mac=','help'])
    except:
        print("Error: Parametros incorrectos.")
        uso()
        
    IP = None
    MAC = None
    extraccion()
    for opt, arg in options:
        if opt in ('--help'):
            uso()
        if opt in ('--ip'  ):
            IP = str(arg)
            macAddres(IP)
        if opt in ('--mac'):
            MAC = str(arg)
            leer(MAC)
        
            
    #MAC y IP deben estar ingresadas.
    if (MAC == None and IP == None):
      print ("Error: Faltan parametros obligatorios.")
      uso()

#
#
#
def uso():
    print("Uso: " + sys.argv[0] + " --ip <ip> || --mac <mac> [--help] ")
    print("\nParametros:")
    print("     --ip: specify the IP of the host to query.")
    print("     --mac: specify the MAC address to query.")
    print("     --help: muestra esta pantalla y termina. Opcional")
    exit(1)
    
#Extraer un txt con la pagina completa de gitlab
def extraccion():
  apiUrl = "https://gitlab.com/wireshark/wireshark/-/raw/master/manuf"
  filename = "test.txt"
  chunk_size = 100
  response = requests.get( apiUrl )
  with open(filename, 'wb') as fd:
    for chunk in response.iter_content(chunk_size):
        fd.write(chunk)
 

def macAddres(IP):
  nombre_equipo = socket.gethostname()
  direccion_equipo = socket.gethostbyname(nombre_equipo)
  if(direccion_equipo == IP):
    mac = get_mac()
    s = '{0:16x}'.format(mac)
    s = ':'.join(re.findall(r'\w\w', s))
    leer (s) 
  else:
    print ("Error: ip is outside the host network")



def leer(MAC):
  enc='utf-8'
  line=[67]
  macs = []
  with open('test.txt','r', encoding=enc) as lineas:
    for line in lineas:
      if MAC in line:
        macs.append(line)
        #retorna un arreglo con un valor
    print ("MAC Addres : "+ MAC)
    if (len(macs) == 0):
      print ("Vendor : Not found")
    else:
      x = macs[0].split('\t')
#    print ("MAC Addres : "+ RATE)
      if (len(x) == 2):
        print ("Vendor : " + x[1])
      else:
        print ("Vendor : " + x[2])
 

#
# Direccion MAC o IP
# Entrada: 
#          MAC: tasa de arribo de paquetes.
#          IP: tiempo maximo de generacion.
# Salida:
#          Mostrar MAC y Vendor
#



#Esto se utiliza para poder importar este codigo en otro script para utilizar sus funciones.
if __name__ == '__main__':
    main()