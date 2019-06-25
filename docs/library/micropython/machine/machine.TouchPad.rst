.. currentmodule:: machine
.. _machine.TouchPad:

.. module:: TouchPad

类 TouchPad -- 触摸
=============================

ESP32 提供了多达 10 个电容式传感 GPIO，能够探测由手指或其他物品直接接触或接近而产生的电容差异。

构建对象
------------

.. class:: TouchPad(Pin)

创建与设定引脚关联的TouchPad对象。

 - ``Pin`` - 可用引脚有：

  =================== =============== ================= =================
  电容式传感信号名称     ESP32 GPIO      掌控板引脚      说明
  =================== =============== ================= =================
  TOUCH0              GPIO4           P28/Touch_N
  TOUCH1              GPIO0           P5/Button_A        引脚上拉不能使用
  TOUCH2              GPIO2           P11/Button_B       引脚上拉不能使用
  TOUCH3              GPIO15          P27/Touch_O
  TOUCH4              GPIO13          P26/Touch_H
  TOUCH5              GPIO12          P25/Touch_T
  TOUCH6              GPIO14          P24/Touch_Y
  TOUCH7              GPIO27          P23/Touch_P
  TOUCH8              GPIO33          P0
  TOUCH9              GPIO32          P1
  =================== =============== ================= =================


 .. Note:: 

  ESP32有10个触摸传感。掌控板有8个触摸能用,其中6个引出至掌控板的正面的触摸盘。有关更多信息，请查看 :ref:`掌控板引脚定义<mPythonPindesc>` 。
 

示例::

    from machine import TouchPad, Pin

    tp = TouchPad(Pin(14))



方法
---------

.. method:: TouchPad.read()

读取TouchPad的电平。

``TouchPad.read`` 返回相对于电容性变量的值。当触摸时，是个较小数字(通常在 *10* 内)，当没有触摸时，是较大数字(大于 *1000*)是常见的。然而，这些值是“相对的”，可以根据电路板和周围不同而变化，因此可能的需要进行一些校准。
注意,如果如果调用其他的非触摸引脚将会导致 ``ValueError`` 。

.. method:: TouchPad.config(value)

设置触摸的阈值

  - ``value`` 整数