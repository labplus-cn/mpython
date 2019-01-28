套接字-TCP
================


什么是socket?
-----

``Socket`` 是网络编程的一个抽象概念。通常我们用一个Socket表示“打开了一个网络链接”，而打开一个Socket需要知道目标计算机的IP地址和端口号，再指定协议类型即可。

TCP协议简介
-----

TCP协议，传输控制协议（Transmission Control Protocol，缩写为 TCP）是一种面向连接的、可靠的、基于字节流的传输层通讯协议，由IETF的RFC 793定义。

TCP通信需要经过创建连接、数据传送、终止连接三个步骤。TCP通信模型中，在通信开始之前，一定要先创建相关连接，才能发送数据，类似于生活中，"打电话""。

套接字在工作时将连接的双方分为服务器端和客户端,即C/S模式,TCP通讯原理如下图:

.. figure:: /images/tutorials/tcp原理.png
    :scale: 90 %
    :align: center

    Socket TCP通讯过程


---------------------------------

TCP编程
-----


本教程的这一部分将介绍如何作为客户端或服务端使用TCP套接字。有关更全面的socket模块的使用，请查阅 :mod:`usocket` 模块。
以下教程需要使用到TCP网络调试工具。下文使用的是IOS的 **Network Test Utility** ，可在APP Store搜索安装，android系统请点击下载。 :download:`Network Test Utility.apk </../docs/tools/com.jca.udpsendreceive.2.apk>` 

TCP客户端
~~~~~~~~


TCP编程的客户端一般步骤是：

1. 创建一个socket，用函数socket()
2. 设置socket属性，用函數setsockopt() , *可选* 
3. 绑定IP地址、端口等信息到socket上，用函数bind() , *可选* 
4. 设置要连接的对方的IP地址和端口等属性 
5. 连接服务器,用函数connect()
6. 收发数据,用函數send()和recv(),或者read()和write()
7. 关闭网络连接


tcpClient示例:

.. code-block:: python
    :linenos:

    import socket
    from mpython import *

    host = "172.25.1.63"          # TCP服务端的IP地址
    port = 5001                   # TCP服务端的端口
    s=None

    mywifi=wifi()                 # 创建wifi类


    # 捕获异常，如果在"try" 代码块中意外中断，则停止关闭套接字
    try:
        mywifi.connectWiFi("ssid","password")                   # WiFi连接，设置ssid 和password
        ip=mywifi.sta.ifconfig()[0]                             # 获取本机IP地址
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # 创建TCP的套接字,也可以不给定参数。默认为TCP通讯方式
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 设置socket属性
        s.connect((host,port))                                  # 设置要连接的服务器端的IP和端口,并连接
        s.send("hello mPython,I am TCP Client")                 # 向服务器端发送数据

        while True:
            data = s.recv(1024)                                 # 从服务器端套接字中读取1024字节数据
            if(len(data) == 0):                                 # 如果接收数据为0字节时,关闭套接字
                print("close socket")
                s.close()                                      
                break
            print(data)
            data=data.decode('utf-8')                         # 以utf-8编码解码字符串
            oled.fill(0)                                      # 清屏
            oled.DispChar(data,0,0)                           # oled显示socket接收数据
            oled.show()                                       # 显示
            s.send(data)                                      # 向服务器端发送接收到的数据

    # 当捕获异常,关闭套接字、网络
    except:
        if (s):
            s.close()                              
        mywifi.disconnectWiFi()

.. Attention:: 

    由于在网络中都是以bytes形式传输的，所以需要注意数据编码与解码。


首先掌控板和手机须连接至同个局域网内。打开Network Test Utility，进入“TCP Server”界面，
TCP Server IP选择手机在该网内的IP地址 ，端口号可设范围0~65535。然后，点击Listen，开始监听端口。
在程序中设置上文选择的TCP服务端IP地址 ``host`` 和端口号 ``port`` ，重启运行程序。

当连接Server成功后，TCP Server会接收到Client发送的文本 ``hello mPython,I am TCP Client`` 。此时您在TCP Server发送文本给Client，掌控板会
接收到文本并将文本显示至oled屏上。


.. image:: /images/tutorials/socket_1.gif
   

TCP服务端
~~~~~~~~


TCP编程的服务端一般步骤是：

1. 创建一个socket，用函数socket()
2. 设置socket属性，用函數setsockopt() , *可选* 
3. 绑定IP地址、端口等信息到socket上，用函数bind() 
4. 开启监听和设置最大监听数,用函数listen()
5. 等待客户端請求一个连接，用函数accept()
6. 收发数据，用函數send()和recv()，或者read()和write() 
7. 关闭网络连接



tcpServer示例:

.. code-block:: python
    :linenos:

    import socket
    from mpython import *

    port=5001                   # TCP服务端的端口,range0~65535
    listenSocket=None              

    mywifi=wifi()               # 创建wifi类

    # 捕获异常，如果在"try" 代码块中意外中断，则停止关闭套接字
    try:
        mywifi.connectWiFi("ssid","password")                                   # WiFi连接，设置ssid 和password
        ip= mywifi.sta.ifconfig()[0]                                            # 获取本机IP地址
        listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        # 创建socket,不给定参数默认为TCP通讯方式
        listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)      # 设置套接字属性参数
        listenSocket.bind((ip,port))                                            # 绑定ip和端口
        listenSocket.listen(3)                                                  # 开始监听并设置最大连接数
        print ('tcp waiting...')
        oled.DispChar("%s:%s" %(ip,port),0,0)                                   # oled屏显示本机服务端ip和端口            
        oled.DispChar('accepting.....',0,16)                                            
        oled.show()

        while True:
            print("accepting.....")
            conn,addr = listenSocket.accept()                                   # 阻塞,等待客户端的请求连接,如果有新的客户端来连接服務器，那麼会返回一个新的套接字专门为这个客户端服务
            print(addr,"connected")                                                         
        
            while True:
                data = conn.recv(1024)                                          # 接收对方发送过来的数据,读取字节设为1024字节
                if(len(data) == 0):
                    print("close socket")
                    conn.close()                                                # 如果接收数据为0字节时,关闭套接字
                    break
                data_utf=data.decode()                                          # 接收到的字节流以utf8编码解码字符串
                print(data_utf)
                oled.DispChar(data_utf,0,48)                                    # 将接收到文本oled显示出来
                oled.show()
                oled.fill_rect(0,48,128,16,0)                                   # 局部清屏
                conn.send(data)                                                 # 返回数据给客户端

    # 当捕获异常,关闭套接字、网络
    except:
        if(listenSocket):
            listenSocket.close()
        mywifi.disconnectWiFi()


首先掌控板和手机须连接至同个局域网内。掌控板重启运行程序，TCP Server端等待Client端连接请求。打开Network Test Utility，进入“TCP Client”界面，填写Remote host和port,即 ``socket.blind(ip,port)``
的IP地址和端口。Connect连接成功后，发送文本，掌控板接收到文本显示至oled屏并将返回至TCP Client端。您可在手机接收界面看到文本从Client->Server，Server->Client的过程。


.. image:: /images/tutorials/socket_2.gif
    :scale: 60 %
    :align: center

