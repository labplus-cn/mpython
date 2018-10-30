TCP套接字
================

大多数互联网的通信都是使用TCP套接字。这些套接字在连接的网络设备之间提供可靠的字节流。
本教程的这一部分将介绍如何作为客户端或服务端使用TCP套接字。

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
            data=data.decode('utf-8')
            display.fill(0)
            display.DispChar(data,0,0)
            display.show()
            ret = s.send(data)
        
    except:
        if (s):
            s.close()
        wlan.disconnect()
        wlan.active(False)

.. image:: /images/tutorials/socket_1.gif



TCP服务端
-----