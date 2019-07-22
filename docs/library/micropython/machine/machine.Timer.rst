.. currentmodule:: machine
.. _machine.Timer:

类 Timer -- 控制硬件定时器
======================================

硬件定时器处理周期和事件的时间。定时器可能是MCU和SoC中最灵活和异构的硬件类型，从一个模型到另一个模型的差别很大。
MicroPython的Timer类定义了在给定时间段内（或在一段延迟后执行一次回调）执行回调的基线操作，并允许特定的板定义更多的非标准行为（因此不能移植到其他板）。

请参阅有关Timer回调的 :ref:`重要约束 <machine_callbacks>` 。

.. note::

    内存不能在irq处理程序（中断）中分配，因此处理程序中引发的异常不会提供太多信息。
    了解 :func:`micropython.alloc_emergency_exception_buf` 如何解决此限制。

构建对象
------------

.. class:: Timer(id, ...)

构造给定id的新计时器对象。

    - ``id`` - 任意正整数



方法
-------

.. method:: Timer.init(\*, mode=Timer.PERIODIC, period=-1, callback=None)


    - ``mode`` - 定时器模式,可以是以下之一:

        - ``Timer.ONE_SHOT`` - 计时器运行一次，直到配置完毕通道的期限到期。
        - ``Timer.PERIODIC`` - 定时器以通道的配置频率定期运行。
    - ``period`` -  定时器执行的周期，单位是ms， 隔period ms 执行一次。 period取值范围： 0 < period <= 3435973836
    - ``callback`` -  定时器的回调函数


初始化计时器，示例::

    tim.init(period=100)                         # periodic with 100ms period
    tim.init(mode=Timer.ONE_SHOT, period=1000)   # one shot firing after 1000ms


.. method:: Timer.value()

获取并返回计时器当前计数值。 

::

    value = tim.value()
    print(value)

.. method:: Timer.deinit()


取消定时器的初始化。停止计时器，并禁用计时器外围设备。


常数
---------

.. data:: Timer.ONE_SHOT
.. data:: Timer.PERIODIC


.. literalinclude:: /../examples/timer/timer_led_blink.py
    :caption: 定时器控制LED闪烁
    :linenos: