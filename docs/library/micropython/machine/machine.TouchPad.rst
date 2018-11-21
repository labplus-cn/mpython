.. currentmodule:: machine
.. _machine.TouchPad:

类 TouchPad -- 触摸
=============================


构建对象
------------

.. class:: TouchPad(Pin)

创建与设定引脚关联的TouchPad对象。

 - ``Pin`` 可用引脚有：``GPIO4``、``GPIO0``、``GPIO2``、``GPIO15``、``GPIO13``、``GPIO12``、``GPIO14``、``GPIO27``、``GPIO33``、``GPIO32``。有关更多信息，请查看 `ESP32引脚功能表. <../../../images/pinout_wroom_pinout.png>`_ 
 

示例::

    from machine import TouchPad, Pin

    tp = TouchPad(Pin(14))



方法
---------

.. method:: TouchPad.read()

读取TouchPad的电平。

.. method:: TouchPad.config(value)

设置触摸板的标识。

  - ``value`` 任意整数值