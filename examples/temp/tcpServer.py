import network
import socket
import time

SSID="dfrobotYanfa"
PASSWORD="hidfrobot"
port=10000
wlan=None
listenSocket=None

def connectWifi(ssid,passwd):
  global wlan
  wlan=network.WLAN(network.STA_IF)         #create a wlan object
  wlan.active(True)                         #Activate the network interface
  wlan.disconnect()                         #Disconnect the last connected WiFi
  wlan.connect(ssid,passwd)                 #connect wifi
  while(wlan.ifconfig()[0]=='0.0.0.0'):
    time.sleep(1)
  return True

#Catch exceptions,stop program if interrupted accidentally in the 'try'
try:
  connectWifi(SSID,PASSWORD)
  ip=wlan.ifconfig()[0]                     #get ip addr
  listenSocket = socket.socket()            #create socket
  listenSocket.bind((ip,port))              #bind ip and port
  listenSocket.listen(1)                    #listen message
  listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    #Set the value of the given socket option
  print ('tcp waiting...')

  while True:
    print("accepting.....")
    conn,addr = listenSocket.accept()       #Accept a connection,conn is a new socket object
    print(addr,"connected")

    while True:
      data = conn.recv(1024)                #Receive 1024 byte of data from the socket
      if(len(data) == 0):
        print("close socket")
        conn.close()                        #if there is no data,close
        break
      print(data)
      ret = conn.send(data)                 #send data
except:
  if(listenSocket):
    listenSocket.close()
  wlan.disconnect()
  wlan.active(False)

