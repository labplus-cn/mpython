.. currentmodule:: machine
.. _machine.RTC:

类 RTC -- 实时时钟
============================

RTC是独立的时钟，可以跟踪日期和时间。

示例::

      import machine
      from machine import RTC 
      rtc = machine.RTC()
      rtc.init((2018, 11, 21, 3, 9, 0, 0, 0))
      print(rtc.datetime())


构建对象
------------

.. class:: RTC()

创建RTC对象。

方法
-------

.. method:: RTC.init([datetimetuple])

始化RTC。日期时间为下列形式的8元组：

( year,month,day,weekday,hour,minute,second,microsecond )

      - ``weekday`` -从周一到周日对应1-7。


.. method:: RTC.datetime([datetimetuple])

设置RTC日期和时间。

8元组格式同上文。


