
.. module:: bluebit
   :synopsis: blue:bit驱动

:mod:`bluebit` --- blue:bit驱动
==================================================


`blue:bit` 模块提供bluebit套件的掌控板库。


.. contents::

.. image:: http://wiki.labplus.cn/images/0/07/Bluebit套件1.png


NTC模块
-------------

.. autoclass:: bluebit.NTC
    :members:
    :undoc-members: True
    :exclude-members: 
    :special-members: '__init__' 
    :member-order: bysource


LM35模块
-------------

.. autoclass:: bluebit.LM35
    :members:
    :undoc-members: True
    :exclude-members: 
    :special-members: '__init__' 
    :member-order: bysource


四按键模块
-------------

.. autoclass:: bluebit.joyButton
    :members:
    :undoc-members: True
    :exclude-members: 
    :special-members: '__init__' 
    :member-order: bysource

温湿度模块
-------------

.. autoclass:: bluebit.SHT20
    :members:
    :undoc-members: True
    :exclude-members: 
    :special-members: '__init__' 
    :member-order: bysource


颜色模块
-------------

.. autoclass:: bluebit.Color
    :members:
    :undoc-members: True
    :exclude-members: 
    :special-members: '__init__' 
    :member-order: bysource

数字光线模块
-------------

.. autoclass:: bluebit.AmbientLight
    :members:
    :undoc-members: True
    :exclude-members: 
    :special-members: '__init__' 
    :member-order: bysource


超声波模块
-------------

.. autoclass:: bluebit.Ultrasonic
    :members:
    :undoc-members: True
    :exclude-members: 
    :special-members: '__init__' 
    :member-order: bysource

4段数码管模块
-------------

.. autoclass:: bluebit.SEGdisplay
    :members:
    :undoc-members: True
    :exclude-members: 
    :special-members: '__init__' 
    :member-order: bysource

8x8点阵模块
-------------

.. py:class:: Matrix(i2c=i2c)

8x8点阵模块控制类

- ``i2c`` : I2C实例对象,默认i2c=i2c. 

.. py:method:: Matrix.blink_rate(rate=None)

设置像素点闪烁率

- ``rate`` : 闪烁间隔时间,单位秒.默认None,常亮.


.. py:method:: Matrix.brightness(brightness)

设置像素点亮度

- ``brightness`` : 亮度级别,范围0~15.


.. py:method:: Matrix.fill(color)

填充所有

-  ``color`` : 1亮;0灭

.. py:method:: Matrix.bitmap(bitmap)

显示位图

-  ``bitmap`` : 8x8点阵数据


.. py:method:: Matrix.show()

显示生效


除上述函数方法外,还继承 ``FrameBuffer`` 类 ,有关其他方法,如显示字符,绘制函数。详情可查阅 micropython framebuf模块 `FrameBuffer <https://mpython.readthedocs.io/zh/master/library/micropython/framebuf.html>`_ 类.

LCD1602模块
-------------

.. autoclass:: bluebit.LCD1602
    :members:
    :undoc-members: True
    :exclude-members: 
    :special-members: '__init__' 
    :member-order: bysource

MIDI模块
-------------

.. autoclass:: bluebit.MIDI
    :members:
    :undoc-members: True
    :exclude-members: 
    :special-members: '__init__' 
    :member-order: bysource



MP3模块
-------------

.. autoclass:: bluebit.MP3
    :members:
    :undoc-members: True
    :exclude-members: 
    :special-members: '__init__' 
    :member-order: bysource


OLED模块
-------------

.. autoclass:: bluebit.OLEDBit
    :members:
    :undoc-members: True
    :exclude-members: 
    :special-members: '__init__' 
    :member-order: bysource


红外接收模块
-------------

.. autoclass:: bluebit.IRRecv
    :members:
    :undoc-members: True
    :exclude-members: 
    :special-members: '__init__' 
    :member-order: bysource

红外发射模块
-------------

.. autoclass:: bluebit.IRTrans
    :members:
    :undoc-members: True
    :exclude-members: 
    :special-members: '__init__' 
    :member-order: bysource


实验探究类
-------------

适用的模块有电压、电流、磁场、电导率、PH、光电门、气压、力传感器。

.. autoclass:: bluebit.DelveBit
    :members:
    :undoc-members: True
    :exclude-members: 
    :special-members: '__init__' 
    :member-order: bysource


编码电机模块
-------------

.. autoclass:: bluebit.EncoderMotor
    :members:
    :undoc-members: True
    :exclude-members: 
    :special-members: '__init__' 
    :member-order: bysource

