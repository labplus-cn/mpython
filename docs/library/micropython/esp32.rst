:mod:`esp32` --- 特定于ESP32的功能
====================================================

.. module:: esp32
    :synopsis: 特定于ESP32的功能

``esp32`` 模块包含专门用于控制ESP32模块的功能和类。

函数
---------

.. function:: wake_on_touch(wake)

    配置触摸是否将设备从睡眠状态唤醒。 wake应该是一个布尔值

.. function:: wake_on_ext0(pin, level)

    配置 `EXT0` 如何将设备从睡眠状态唤醒。 

    - ``pin`` :None 或者 有效的Pin对象。 
    - ``level`` : ``esp32.WAKEUP_ALL_LOW`` 或 ``esp32.WAKEUP_ANY_HIGH`` 。

.. function:: wake_on_ext1(pins, level)

    配置 `EXT1` 如何将设备从睡眠状态唤醒。 

    - ``pin`` :None 或者 有效的Pin对象的元组/列表。 
    - ``level`` : ``esp32.WAKEUP_ALL_LOW`` 或 ``esp32.WAKEUP_ANY_HIGH`` 。

.. function:: raw_temperature()

    读取内部温度传感器的原始值，返回一个整数。

.. function:: hall_sensor()

    读取内部霍尔传感器的原始值，返回一个整数。


超低功耗协处理器
--------------------------------

.. class:: ULP()

    该类提供对超低功耗协处理器的访问。

.. method:: ULP.set_wakeup_period(period_index, period_us)

    设置唤醒时间。

.. method:: ULP.load_binary(load_addr, program_binary)

    在给定的load_addr中将program_binary加载到ULP中。

.. method:: ULP.run(entry_point)

    启动在给定entry_point运行的ULP 。


Constants
---------

.. data:: esp32.WAKEUP_ALL_LOW
          esp32.WAKEUP_ANY_HIGH

   选择引脚的唤醒级别。
