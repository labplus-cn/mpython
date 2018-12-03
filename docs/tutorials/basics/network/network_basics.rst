网络基础
==============

.. _network_base:

MicroPython :mod:`network` 模块用于配置WiFi连接。有两个WiFi接口，STA模式即工作站模式（ESP32连接到路由器），
AP模式提供接入服务（其他设备连接到ESP32）。如需了解MicroPython的网络连接方法，请查阅 :mod:`network` 模块。

掌控板以基于network模块封装 :ref:`mpython.wifi()<mpython.wifi>` 类简化wifi连接设置::

    from mpython import *       #导入mpython模块

    mywifi=wifi()     #实例化wifi类
    mywifi.connectWiFi("ssid","password")  # WiFi连接，设置ssid 和password

.. Note:: 

    实例化wifi()后，会构建 ``sta`` 和 ``ap`` 两个对象。 ``sta`` 对象为工作站模式，通过路由器连接至网络。``ap`` 为AP模式，提供热点接入。

连接成功后Repl串口如下打印::

    Connecting to network...
    Connecting to network...
    WiFi Connection Successful,Network Config:('192.168.0.2', '255.255.255.0', '192.168.0.1', '192.168.0.1')


断开WiFi连接::

    mywifi.disconnectWiFi()



查询WiFi连接信息
-------------------------

查询wifi连接是否已建立::

    mywifi.sta.isconnected()

.. Note:: 如已建立连接，返回 ``True`` ,否则 ``False`` 。

您可以通过以下方式查看网络设置::

    mywifi.sta.ifconfig()

.. Note:: 返回值4元组: (IP address, netmask, gateway, DNS)
    



一旦设置了WiFi，访问网络的方式就是使用套接字。
套接字表示网络设备上的端点，当两个套接字连接在一起时，可以继续进行通信。
Internet协议构建在套接字之上，例如电子邮件（SMTP），Web（HTTP），telnet，ssh等等。
为这些协议中的每一个分配一个特定的端口，它只是一个整数。给定IP地址和端口号，您可以连接到远程设备并开始与之通信。

本教程的下一部分将讨论如何使用套接字来执行一些常见且有用的网络任务。