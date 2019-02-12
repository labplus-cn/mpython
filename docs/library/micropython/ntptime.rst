
.. _ntptime:
:mod:`ntptime` --- 时间同步
=========================================

该模块用于时间同步,提供准确时间，国际标准时间(UTC)。

.. admonition:: 什么是NTP

    Network Time Protocol（NTP）是用来使计算机时间同步化的一种协议，它可以使计算机对其服务器或时钟源（如石英钟，GPS等等)做同步化。它可以提供高精准度的时间校正。

方法
------


.. method:: settime(timezone=8,server = 'ntp.ntsc.ac.cn')

同步本地时间

    - ``timezone`` - 时区时间差,默认为东八区,补偿8小时
    - ``server``  -  可自行指定授时服务器,server为字符串类型。默认授时服务器为"ntp.ntsc.ac.cn"。


示例::

    from mpython import *
    import ntptime

    mywifi=wifi()
    mywifi.connectWiFi('tang','tang123456')        

    print("同步前本地时间：%s" %str(time.localtime()))
    ntptime.settime()
    print("同步后本地时间：%s" %str(time.localtime()))

运行结果::

    Connecting to network...
    WiFi Connection Successful,Network Config:('172.20.10.4', '255.255.255.240', '172.20.10.1', '172.20.10.1')
    同步前本地时间：(2000, 1, 1, 0, 40, 8, 5, 1)
    同步后本地时间：(2018, 12, 27, 12, 10, 7, 3, 361)
    MicroPython v1.0.1-dirty on 2018-11-23; mPython with ESP32
    Type "help()" for more information.
    >>>