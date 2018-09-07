****************************************
:mod:`network` --- 网络配置
****************************************

.. module:: network
   :synopsis: 网络配置


该模块提供网络驱动程序和路由配置。要使用此模块，必须烧录具有网络功能的MicroPython固件版本。
此模块中提供了特定硬件的网络驱动程序，用于配置硬件网络接口。然后，可以通过 :mod:`usocket`
模块使用已配置接口提供的网络服务。

构建函数
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

常量
---------

.. data:: WLAN.STA
.. data:: WLAN.AP

