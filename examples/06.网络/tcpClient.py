import network
import time
import socket
from mpython import *

host = "172.25.1.63"          #TCP Server IP
port = 5001                     #Port
s=None

mywifi=wifi()     #实例化wifi类


#Catch exceptions,stop program if interrupted accidentally in the 'try'
try:
    mywifi.connectWiFi("ssid","password")                  # WiFi连接，设置ssid 和password
    ip=mywifi.sta.ifconfig()[0]                                #get ip addr
    s = socket.socket()                                   #create socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#Set the value of the given socket option
    s.connect((host,port))                                #send require for connect
    s.send("hello mPython,I am TCP Client")               #send data

    while True:
        data = s.recv(1024)                               #Receive 1024 byte of data from the socket
        if(len(data) == 0):                               #if there is no data,close
            print("close socket")
            s.close()
            break
        print(data)
        data=data.decode()                                #以utf-8编码解码字符串
        oled.fill(0)
        oled.DispChar(data,0,0)
        oled.show()
        ret = s.send(data)

except:
    if (s):
        s.close()
    mywifi.disconnectWiFi()