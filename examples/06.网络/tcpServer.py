import network
import socket
import time
from mpython import *

SSID="yourSSID"
PASSWORD="yourPASSWORD"
port=5001
wlan=None
listenSocket=None

# 本函数实现wifi连接 
def ConnectWifi(ssid,passwd):
        global wlan
        wlan=network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.disconnect()
        wlan.connect(ssid,passwd)
  
        while(wlan.ifconfig()[0]=='0.0.0.0'):
                time.sleep(1)
                print('Connecting to network...')
        print('WiFi Connection Successful,Network Config:%s' %str(wlan.ifconfig()))

#Catch exceptions,stop program if interrupted accidentally in the 'try'
try:
    ConnectWifi(SSID,PASSWORD)
    ip=wlan.ifconfig()[0]                     #get ip addr
    listenSocket = socket.socket()            #create socket
    listenSocket.bind((ip,port))              #bind ip and port
    listenSocket.listen(1)                    #listen message
    listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    #Set the value of the given socket option
    print ('tcp waiting...')
    display.DispChar("%s:%s" %(ip,port),0,0)
    display.DispChar('accepting.....',0,16)
    display.show()
  
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
            ret = conn.send(data)                 #return data to client
except:
    if(listenSocket):
        listenSocket.close()
    wlan.disconnect()
    wlan.active(False)

