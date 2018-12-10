****************************************
:mod:`network` --- 网络配置
****************************************

.. module:: network
   :synopsis: 网络配置


该模块提供网络驱动程序和路由配置。要使用此模块，必须烧录具有网络功能的MicroPython固件版本。
此模块中提供了特定硬件的网络驱动程序，用于配置硬件网络接口。然后，可以通过 :mod:`usocket`
模块使用已配置接口提供的网络服务。

构建对象
------------

.. class:: WLAN(interface_id)

  创建WLAN对象。

- ``interface_id`` 

  - ``network.STA_IF`` 客户端，连接到上游WiFi接入点。
  - ``network.AP_IF``  接入点，允许其他WiFi客户端连接。



方法
------------

.. method:: WLAN.active(is_active)

带有参数时，为是否激活界面，不带参数为查询当前状态。

- ``is_active`` 

  -  ``True``  激活（“up”）网络接口。
  -  ``False``  停用（“down”）网络接口。


.. method:: WLAN.scan([ssid，bssid，channel，RSSI，authmode，hidden])

扫描可用的无线网络（仅在STA接口上进行扫描），返回有关WiFi接入点信息的元组列表。

- ``ssid`` 服务集标识。

- ``bssid`` 接入点的硬件地址，以二进制形式返回为字节对象。您可以使用ubinascii.hexlify()将其转换为ASCII格式。

- ``authmode``

  - ``AUTH_OPEN`` = 0
  - ``AUTH_WEP`` = 1
  - ``AUTH_WPA_PSK`` = 2
  - ``AUTH_WPA2_PSK`` = 3
  - ``AUTH_WPA_WPA2_PSK`` = 4
  - ``AUTH_MAX`` = 6
	
- ``hidden``

  - ``False`` 可见
  - ``True`` 隐藏
  
.. method:: WLAN.isconnected()

检查站点是否连接到AP。

- 在STA模式下，如果连接到WiFi接入点并具有有效的IP地址则返回True，否则返回False。
- 在AP模式下，当站点连接时返回True，否则返回False。

.. method::  WLAN.connect(ssid, password)

连接到无线网络。

- ``ssid``：WiFi名称
- ``password``：WiFi密码

.. method::  WLAN.config(essid, channel)

获取接口的MAC adddress或者设置WiFi接入点名称和WiFi通道。

-  ``ssid``：WiFi账户名
-  ``channel``：WiFi通道

.. method::  WLAN.ifconfig([(ip, subnet, gateway, dns)])

不带参数时，返回一个4元组(ip, subnet_mask, gateway, DNS_server)。

- ``ip``：IP地址
- ``subnet_mask``：子网掩码
- ``gateway``:网关
- ``DNS_server``：DNS服务器


带参数时，配置静态IP。例如::

  wlan.ifconfig('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8')


.. method:: WLAN.disconnect()

断开与当前连接的无线网络的连接。

.. method:: WLAN.status()

返回无线连接的当前状态。


示例
------------



作为客户端连接WiFi::

  import network

  SSID = "yourSSID"                  #WiFi名称
  PASSWORD = "yourPASSWD"            #WiFi密码

  wlan = network.WLAN(network.STA_IF)  #创建WLAN对象
  wlan.active(True)                  #激活界面
  wlan.scan()                        #扫描接入点
  wlan.isconnected()                 #检查站点是否连接到AP
  wlan.connect(SSID, PASSWORD)       #连接到AP
  wlan.config('mac')                 #获取接口的MAC adddress
  wlan.ifconfig()                    #获取接口的IP/netmask/gw/DNS地址



作为接入开启WiFi::

  import network

  ap = network.WLAN(network.AP_IF)     #创建接入点界面
  ap.active(True)                      #激活界面
  ap.config(essid='ESP-AP',channel=1)  #设置接入点的ESSID，和WiFi 通道

  

WiFi连接实例::

  import network

  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('SSID', 'PASSWORD')   #连接到AP
      #'SSID'： WiFi账号名
      #'PASSWORD'：WiFi密码
    while not wlan.isconnected():
      pass
  print('network config:', wlan.ifconfig())