
import urequests
import network
import socket
import time
import json
from mpython import *


host = "172.25.1.63"
port = 100


try:
  connectWifi()
  ip=wlan.ifconfig()[0]                                 #get ip addr
  s = socket.socket()                                   #create socket
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#Set the value of the given socket option
  s.connect((host,port))                                #send require for connect
  s.send("hello DFRobot,I am TCP Client")               #send data
  
  while True:
    data = s.recv(1024)                               #Receive 1024 byte of data from the socket
    if(len(data) == 0):                               #if there is no data,close
      print("close socket")
      s.close()
      break
    data=data.decode('utf-8')
    print(data)
    display.fill(0)
    display.DispChar(data,0,0)
    display.show()
    ret = s.send(data)
    
except:
  if (s):
    s.close()
  wlan.disconnect()
  wlan.active(False)
