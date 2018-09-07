.. currentmodule:: machine
.. _machine.TouchPad:

类 TouchPad -- 触摸
=============================


构建函数
------------

.. class:: TouchPad(Pin)

创建与设定引脚关联的TouchPad对象。

 - ``Pin`` 可用引脚有：``GPIO4``、``GPIO0``、``GPIO2``、``GPIO15``、``GPIO13``、``GPIO12``、``GPIO14``、``GPIO27``、``GPIO33``、``GPIO32``。有关更多信息，请查看 `ESP32引脚功能表. <../../../images/esp32_pinout.png>`_ 
 

示例::

    from machine import TouchPad, Pin

    tp = TouchPad(Pin(12))



方法
---------

.. method:: TouchPad.read()

读取TouchPad的电平。若TouchPad接高电平则返回1，若接GND则返回0。 

.. method:: config(value)

设置触摸板的标识。

  - ``value`` 任意整数值