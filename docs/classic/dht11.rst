DHT11读取温湿度
==========


DHT11数字温湿度传感器是一款含有已校准数字信号输出的温湿度复合传感器，它应用专用的数字模块采集技术和温湿度传感技术，确保产品具有极高的可靠性和卓越的长期稳定性。传感器包括一个电阻式感湿元件和一个NTC测温元件，并与一个高性能8位单片机相连接。因此该产品具有品质卓越、超快响应、抗干扰能力强、性价比极高等优点。

.. image:: /images/classic/dht11.png
    :scale: 50 %
    :align: center

DHT11数字温湿度传感器和掌控板连接需要借助掌控扩展版，在掌控扩展版中DHT11可使用的引脚有0/1/2/8/9/13/14/15/16，在这里使用引脚0。将掌控板插在掌控扩展板上，通过双母头杜邦线将DHT11和扩展板进行连接，DHT11上的“+”连接扩展板的电源口“V”，“-”连接扩展板的地线口“G”，“out”连接扩展板的引脚“0”。

.. image:: /images/classic/dhtconnect.jpg
    :scale: 60 %
    :align: center


例：显示DHT11读取的温湿度
::

    from mpython import *
    from dht import DHT11
    
    dht=DHT11(Pin(Pin.P0))

    while True:
        dht.measure()
        oled.fill(0)
        oled.DispChar("温度:",0,10)
        oled.text("%d" % (dht.temperature()), 48, 14)
        oled.DispChar("湿度:",0,35)
        oled.text("%d" % (dht.humidity()), 48, 40)
        oled.show()
        sleep_ms(100)

.. image:: /images/classic/dhtexample.jpg
    :scale: 60 %
    :align: center


使用前，导入mpython模块和DHT11类::

  from mpython import *
  from dht import DHT11

实例化DHT11类，并设置mPython引脚P0::

  dht=DHT11(Pin(Pin.P0))

DHT11测量并返回温湿度数据::

  dht.measure()
  dht.temperature()
  dht.humidity()

.. Note::

  ``dht.measure()`` 为DHT11测量温湿度数据指令，测量后使用 ``dht.temperature()`` 、 ``dht.humidity()`` 获取测量的温湿度值。