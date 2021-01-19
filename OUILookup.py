#!/usr/bin/env python

# Script que genera tiempos aleatorios de llegada de paquetes con
# una tasa de arribo --rate, entre 0 y --maxtime segundos.

# Modo de uso:
#
# Uso: ./random-test.py --ip <ip> | --mac <maximum time> [--help] 
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
        
            
    #RATE y MAX_TIME deben estar ingresadas.
    if (MAC == None and IP == None):
      print ("Error: Faltan parametros obligatorios.")
      print ("test")
      uso()

    
    
    #Ahora se pasa al programa
    #eventos = []
    #genEvents(RATE, eventos)
    
    #showEvents(eventos)

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
 # leer('00:00:00')

def macAddres(IP):
 # encoding = 'utf-8'
 # IP = "192.168.1.30"
 # pid = Popen(["arp", "-n", IP], stdout=PIPE)
 # s = pid.communicate()[0]
 # MAC = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s).groups()[0]
 # MAC.decode(encoding)
 # leer(MAC)
  nombre_equipo = socket.gethostname()
  direccion_equipo = socket.gethostbyname(nombre_equipo)
  if(direccion_equipo == IP):
#  print ('La IP es: ' + direccion_equipo)
    mac = get_mac()
    s = '{0:16x}'.format(mac)
    s = ':'.join(re.findall(r'\w\w', s))
    leer (s)
#  print (mac)
    
#  print(s)
    
  else:
    print ("Error: ip is outside the host network")



def leer(MAC):
  enc='utf-8'
  line=[67]
  #i=0
  #f=open('test.txt')
  #for line in f:
  #  #print (line)
  #   i+=1  
#busca RATE(mac) en el test.txt y lo almacena en macs[]
  #MAC = input()
 # MAC = '00:00:00'
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
# Genera Eventos
# Entrada: 
#          rate: tasa de arribo de paquetes.
#          maxTime: tiempo maximo de generacion.
# Salida:
#          eventos : lista que contiene los tiempos de los eventos generados.
#



#Esto se utiliza para poder importar este codigo en otro script para utilizar sus funciones.
if __name__ == '__main__':
    main()