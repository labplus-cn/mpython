.. currentmodule:: machine
.. _machine.RTC:

类 RTC -- 实时时钟
============================

RTC是一个独立的时钟，用来记录日期和时间。

示例::

    rtc = machine.RTC()
    rtc.init((2014, 5, 1, 4, 13, 0, 0, 0))
    print(rtc.now())


构建对象
------------

.. class:: RTC(id=0, ...)

创建RTC对象。请参阅init以获取初始化参数。

方法
-------

.. method:: RTC.init(datetime)

   初始化RTC。Datetime是表单的元组：
   
      ``(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])``

.. method:: RTC.now()

   获取当前日期时间元组。

.. method:: RTC.deinit()

   将RTC重置为2015年1月1日，并重新开始运行。

.. method:: RTC.alarm(id, time, \*, repeat=False)

设置RTC警报。时间可能是一个毫秒值，可以将警报设置为毫秒值当前时间+未来的time_in_ms，或datetime元组。如果时间过去了
毫秒时， ``repeat`` 可以设置为 ``True`` ，使警报具有周期性。

.. method:: RTC.alarm_left(alarm_id=0)

   获取警报到期前剩余的毫秒数。

.. method:: RTC.cancel(alarm_id=0)

   取消正在运行的警报。

.. method:: RTC.irq(\*, trigger, handler=None, wake=machine.IDLE)

   创建由实时时钟警报触发的irq对象。

      - ``trigger`` 一定是 ``RTC.ALARM0``
      - ``handler`` 是触发回调时要调用的函数。
      - ``wake`` 指定此中断可唤醒系统的睡眠模式。

常数
---------

.. data:: RTC.ALARM0

    irq触发源
