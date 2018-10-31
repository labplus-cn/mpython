TCP套接字
================

大多数互联网的通信都是使用TCP套接字。这些套接字在连接的网络设备之间提供可靠的字节流。
本教程的这一部分将介绍如何作为客户端或服务端使用TCP套接字。有关更全面的socket模块的使用，请查阅 :mod:`usocket` 模块。

以下教程需要使用到TCP网络调试工具。下文使用的是IOS的 **Network Test Utility** ，可在APP Store搜索安装，android系统请点击下载。 :download:`Network Test Utility.apk </../docs/tools/com.jca.udpsendreceive.2.apk>` 

TCP客户端
-----

tcpClient示例::

    import network
    import time
    import socket
    from mpython import *

    # wifi参数 
    SSID="yourSSID"                 #wifi名称
    PASSWORD="yourPSW"              #密码
    host = "172.25.1.63"          #TCP Server IP
    port = 5001                     #Port
    s=None
    wlan=None

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
        ip=wlan.ifconfig()[0]                                 #get ip addr
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
            display.fill(0)
            display.DispChar(data,0,0)
            display.show()
            ret = s.send(data)
        
    except:
        if (s):
            s.close()
        wlan.disconnect()
        wlan.active(False)



首先掌控板和手机须连接至同个局域网内。打开Network Test Utility，进入“TCP Server”界面，
TCP Server IP选择手机在该网内的IP地址 ，端口号可设范围0~65535。然后，点击Listen，开始监听端口。
在程序中设置上文选择的TCP服务端IP地址 ``host`` 和端口号 ``port`` ，重启运行程序。

当连接Server成功后，TCP Server会接收到Client发送的文本 ``hello mPython,I am TCP Client`` 。此时你在TCP Server发送文本给Client，掌控板会
接收到文本并将文本显示至oled屏上。


.. image:: /images/tutorials/socket_1.gif
   

TCP服务端
-----

tcpServer示例::

    import network
    import socket
    import time
    from mpython import *

    SSID="youSSID"
    PASSWORD="yourPSW"
    port=5001               # TCP Sever port,range0~65535
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
                data_utf=data.decode()                  #以utf8编码解码字符串
                print(data_utf)
                display.DispChar(data_utf,0,48)         #将接收到文本显示出来
                display.show()
                display.fill_rect(0,48,128,16,0)        #局部清屏
                ret = conn.send(data)                    #return data to client
    except:
        if(listenSocket):
            listenSocket.close()
        wlan.disconnect()
        wlan.active(False)


首先掌控板和手机须连接至同个局域网内。掌控板重启运行程序，TCP Server端等待Client端连接请求。打开Network Test Utility，进入“TCP Client”界面，填写Remote host和port,即 ``socket.blind(ip,port)``
的IP地址和端口。Connect连接成功后，发送文本，掌控板接收到文本显示至oled屏并将返回至TCP Client端。你可在手机接收界面看到文本从Client->Server，Server->Client的过程。


.. image:: /images/tutorials/socket_2.gif
    :scale: 60 %
    :align: center

