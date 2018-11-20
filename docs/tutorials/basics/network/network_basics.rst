网络基础
==============

.. _network_base:

:mod:`network` 模块用于配置WiFi连接。有两个WiFi接口，STA模式即工作站模式（ESP32连接到路由器），
AP模式提供接入服务（其他设备连接到ESP32）。有关更多使用，请查阅 :mod:`network` 模块。

使用以下方法创建这些对象::

    >>> import network
    >>> sta_if = network.WLAN(network.STA_IF)    #create network obj,STA mode
    >>> ap_if = network.WLAN(network.AP_IF)      #create network obj,AP mode

您可以通过以下方式检查接口是否处于活动状态::

    >>> sta_if.active()
    False
    >>> ap_if.active()
    False

您还可以通过以下方式查看网络设置::

    >>> ap_if.ifconfig()
    ('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8')

返回值有: IP address, netmask, gateway, DNS.

配置 WiFi
-------------------------

您可以使用STA_IF接口将模块配置为连接到您自己的网络。

首先激活STA_IF接口::

    >>> sta_if.active(True)

连接你的 WiFi 网络，需要设置你的WiFi名称和密码::

    >>> sta_if.connect('<your ESSID>', '<your password>')

要检查连接是否已建立::

    >>> sta_if.isconnected()

一旦建立，您可以检查IP地址::

    >>> sta_if.ifconfig()
    ('192.168.0.2', '255.255.255.0', '192.168.0.1', '8.8.8.8')

如果不再需要连接WiFi，可以禁用STA_IF接口::

    >>> sta_if.active(False)

下面是一个连接WiFi的函数你可以执行它，或者放在boot.py文件。这样就可以实现启动自动连接到您的WiFi网络::

    def do_connect():
        import network
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            print('connecting to network...')
            sta_if.active(True)
            sta_if.connect('<essid>', '<password>')
            while not sta_if.isconnected():
                pass
        print('network config:', sta_if.ifconfig())

Sockets
-------

一旦设置了WiFi，访问网络的方式就是使用套接字。
套接字表示网络设备上的端点，当两个套接字连接在一起时，可以继续进行通信。
Internet协议构建在套接字之上，例如电子邮件（SMTP），Web（HTTP），telnet，ssh等等。
为这些协议中的每一个分配一个特定的端口，它只是一个整数。给定IP地址和端口号，您可以连接到远程设备并开始与之通信。

本教程的下一部分将讨论如何使用套接字来执行一些常见且有用的网络任务。