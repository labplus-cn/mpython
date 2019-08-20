.. module:: mpython_classroom_kit
   :synopsis: 掌控板实验箱模块

:mod:`mpython_classroom_kit` --- 掌控板实验箱模块
==========================================================

``mpython_classroom_kit`` 模块提供实验箱上的传感器和输出设备的驱动函数,及人工智能应用的相关函数。

函数
---------


.. function:: get_distance()

获取超声波传感器测距值,单位cm。范围3~340CM


.. function:: set_motor(speed)

设置马达速度

-  ``speed`` - 马达速度,范围±100。正值表示正转,负值则反。


.. function:: get_key()

获取方向按键,返回已按下按键的集合。当单个或多个按键按下,可以集合(set)运算,判断按键状态。

集合所有元素如下: 
`{'left', 'right', 'up', 'down', 'ok'}`

.. literalinclude:: /../examples/mpython_classroom_kit/key_control_motor.py
    :caption: 方向按键控制马达
    :linenos:


.. method:: pir.value()

返回人体红外触发值。当为1时,表示已触发。

.. method:: slider_res.read()

返回滑杆电阻采样值。范围0~4095。

.. literalinclude:: /../examples/mpython_classroom_kit/slider_control_motor.py
    :caption: 滑杆控制马达
    :linenos:

AI类
------------