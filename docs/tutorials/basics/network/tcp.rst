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

声明：这里的TCP客户端（tcpClient）是你的电脑或者手机，而TCP服务端（tcpServer）是mpython掌控板。

TCP客户端
~~~~~~~~


TCP编程的客户端一般步骤是：

1. 创建一个socket，用函数socket()
2. 设置socket属性，用函数setsockopt() , *可选* 
3. 绑定IP地址、端口等信息到socket上，用函数bind() , *可选* 
4. 设置要连接的对方的IP地址和端口等属性 
5. 连接服务器,用函数connect()
6. 收发数据,用函数send()和recv(),或者read()和write()
7. 关闭网络连接



.. literalinclude:: /../examples/06.网络/tcpClient.py
    :caption: TCP Client示例:
    :linenos:


.. Attention:: 

    由于在网络中都是以bytes形式传输的，所以需要注意数据编码与解码。

.. Attention:: 上例,使用 ``connectWiFi()`` 连接同个路由器wifi。你也可以用 ``enable_APWiFi()`` 开启AP模式,自建wifi网络让其他设备接入进来。

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
2. 设置socket属性，用函数setsockopt() , *可选* 
3. 绑定IP地址、端口等信息到socket上，用函数bind() 
4. 开启监听和设置最大监听数,用函数listen()
5. 等待客户端請求一个连接，用函数accept()
6. 收发数据，用函数send()和recv()，或者read()和write() 
7. 关闭网络连接



tcpServer示例:

.. literalinclude:: /../examples/06.网络/tcpServer.py
    :caption: TCP Server示例:
    :linenos:


.. Attention:: 上例,使用``connectWiFi()`` 连接同个路由器wifi。你也可以用 ``enable_APWiFi()`` 开启AP模式,自建wifi网络让其他设备接入进来。

首先掌控板和手机须连接至同个局域网内。掌控板重启运行程序，TCP Server端等待Client端连接请求。打开Network Test Utility，进入“TCP Client”界面，填写Remote host和port,即 ``socket.blind(ip,port)``
的IP地址和端口。Connect连接成功后，发送文本，掌控板接收到文本显示至oled屏并将返回至TCP Client端。您可在手机接收界面看到文本从Client->Server，Server->Client的过程。


.. image:: /images/tutorials/socket_2.gif
    :scale: 60 %
    :align: center

