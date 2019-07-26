
:mod:`network` --- 网络配置
===============================

.. module:: network
   :synopsis: 网络配置


该模块提供网络驱动程序和路由配置。此模块中提供了特定硬件的网络驱动程序，用于配置硬件网络接口。然后，可以通过 :mod:`usocket`
模块使用已配置接口提供的网络服务。


函数
-----

.. function:: phy_mode([mode])

    设置PHY模式。定义的模式常量如下:

    - ``mode``

      - ``MODE_11B`` -- IEEE 802.11b,1
      - ``MODE_11G`` -- IEEE 802.11g,2
      - ``MODE_11N`` -- IEEE 802.11n,4


WLAN类
---------

此类为ESP32中的WiFi网络处理器提供驱动程序。用法示例::

  import network
  # enable station interface and connect to WiFi access point
  nic = network.WLAN(network.STA_IF)
  nic.active(True)
  nic.connect('your-ssid', 'your-password')
  # now use sockets as usual


构建对象
~~~~~~~~~~~

.. class:: WLAN(interface_id)

  创建WLAN网络接口对象。

- ``interface_id`` 

  - ``network.STA_IF`` 站点也称为客户端，连接到上游WiFi接入点
  - ``network.AP_IF``  作为热点，允许其他WiFi客户端接入。热点模式允许用户将自己的设备配置为热点，这让多个设备之间的无线连接在不借助外部路由器网络的情况下成为可能。

以下方法的可用性取决于接口类型。例如，只有STA接口可以 ``connect()`` 到达接入点。

方法
------------

.. method:: WLAN.active(is_active)

带有参数时，为是否激活，不带参数为查询当前状态。当激活WiFi功能后,功耗会增加。当不使用WiFi功能可使用 ``active`` 来真正关闭物理层的无线。

- ``is_active`` 

  -  ``True``  激活网络接口
  -  ``False``  停用网络接口


.. method::  WLAN.connect(ssid, password)

使用指定的密码连接到指定的无线网络

- ``ssid``：WiFi名称
- ``password``：WiFi密码


.. method:: WLAN.disconnect()

断开当前连接的无线网络。



.. method:: WLAN.scan([ssid，bssid，channel，RSSI，authmode，hidden])

扫描可用的无线网络（仅在STA接口上进行扫描），返回有关WiFi接入点信息的元组列表。

- ``ssid`` 服务集标识。
- ``bssid`` 接入点的硬件地址，以二进制形式返回为字节对象。您可以使用 ``ubinascii.hexlify()`` 将其转换为ASCII格式。
- ``channel`` 信道
- ``RSSI`` 信号强度
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
  


.. method:: WLAN.status()

返回无线连接的当前状态。

  - ``STAT_IDLE`` -- 没有连接，没有活动-1000
  - ``STAT_CONNECTING`` -- 正在连接-1001
  - ``STAT_WRONG_PASSWORD`` -- 由于密码错误而失败-202
  - ``STAT_NO_AP_FOUND`` -- 失败，因为没有接入点回复,201
  - ``STAT_GOT_IP`` -- 连接成功-1010
  - ``STAT_ASSOC_FAIL`` -- 203
  - ``STAT_BEACON_TIMEOUT`` -- 超时-200 
  - ``STAT_HANDSHAKE_TIMEOUT`` -- 握手超时-204 



.. method:: WLAN.isconnected()

- 在STA模式下，如果连接到WiFi接入点并具有有效的IP地址则返回True，否则返回False。
- 在AP模式下，当站点连接时返回True，否则返回False。



.. method::  WLAN.ifconfig([(ip, subnet, gateway, dns)])

不带参数时，返回一个4元组(ip, subnet_mask, gateway, DNS_server)。

- ``ip``：IP地址
- ``subnet_mask``：子网掩码
- ``gateway``:网关
- ``DNS_server``：DNS服务器


带参数时，配置静态IP。例如::

  wlan.ifconfig(('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8'))



.. method:: wlan.config('param')
.. method:: wlan.config(param=value, ...)

获取或设置常规网络接口参数。这些方法允许使用超出标准IP配置的其他参数（如所处理 ``wlan.ifconfig()`` ）。 
这些包括特定于网络和硬件的参数。对于设置参数，应使用关键字参数语法，可以一次设置多个参数。

  =========  ===========
  mac        MAC address (bytes)
  essid      WiFi access point name (string)
  channel    WiFi channel (integer)
  hidden     Whether ESSID is hidden (boolean)
  authmode   Authentication mode supported (enumeration, see module constants)
  password   Access password (string)
  =========  ===========



对于查询，参数名称应该作为字符串引用，并且只有一个参数可以查询::

  # Set WiFi access point name (formally known as ESSID) and WiFi channel
  ap.config(essid='My AP', channel=11)
  # Queey params one by one
  print(ap.config('essid'))
  print(ap.config('channel'))

  Following are commonly supported parameters (availability of a specific parameter
  depends on network technology type, driver, and MicroPython port).







示例
------------



STA模式,接入WiFi网络::

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



热点模式::

  import network

  ap = network.WLAN(network.AP_IF)     #创建接入点界面
  ap.active(True)                      #激活界面
  ap.config(essid='micropython',password=b"micropython",channel=11,authmode=network.AUTH_WPA_WPA2_PSK)  #设置接入点



