import network
import socket
import time
from mpython import *

port=5001               # TCP Sever port,range0~65535
listenSocket=None

mywifi=wifi()     #实例化wifi类

#Catch exceptions,stop program if interrupted accidentally in the 'try'
try:
    mywifi.connectWiFi("ssid","password")                  # WiFi连接，设置ssid 和password
    ip= mywifi.sta.ifconfig()[0]                     #get ip addr
    listenSocket = socket.socket()            #create socket
    listenSocket.bind((ip,port))              #bind ip and port
    listenSocket.listen(1)                    #listen message
    listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    #Set the value of the given socket option
    print ('tcp waiting...')
    oled.DispChar("%s:%s" %(ip,port),0,0)
    oled.DispChar('accepting.....',0,16)
    oled.show()

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
            data_utf=data.decode()                  #以utf8编码解码字符串
            print(data_utf)
            oled.DispChar(data_utf,0,48)         #将接收到文本显示出来
            oled.show()
            oled.fill_rect(0,48,128,16,0)        #局部清屏
            ret = conn.send(data)                    #return data to client
except:
    if(listenSocket):
        listenSocket.close()
    mywifi.disconnectWiFi()