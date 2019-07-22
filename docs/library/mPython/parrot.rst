
.. module:: parrot
   :synopsis: 掌控拓展板驱动

:mod:`parrot` --- 掌控拓展板驱动
==================================================

掌控拓展板parrot是mPython掌控板衍生的一款体积小巧、易于携带。支持电机驱动、语音播放、语音合成等功能的IO引脚扩展板,可扩展12路IO接口和2路I2C接口。
该库为掌控拓展板提供电机驱动,LED驱动等功能。

电机控制I2C通讯协议数据格式:

======== ======== =========== ===========
Type     Command   motor_no   speed(int)
控制电机  0x01      0x01/0x02  -100~100
======== ======== =========== ===========

*当 'speed' 为负值,反转；当为正值,正转。*

--------------------------------------------------

.. automodule:: parrot
   :members:
   :member-order: bysource


.. literalinclude:: /../examples/motor_simple.py
    :caption: 电机驱动示例
    :linenos:
