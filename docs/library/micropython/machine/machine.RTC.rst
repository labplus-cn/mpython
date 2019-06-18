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

初始化RTC。日期时间为下列形式的8元组：

( year,month,day,weekday,hour,minute,second,microsecond )


.. Attention:: 

    *  ``weekday``: 星期一到星期天分别对应的是 [0-6] 而不是 [1-7]
    * 毫秒部分的数值其实是秒数的小数点位后的数值


.. method:: RTC.datetime([datetimetuple])

当给定时间元组时为设置RTC日期和时间,未给定参数为返回当前时间元组。8元组格式同上文。


::

    >>> rtc.datetime()
    (2018, 11, 18, 6, 12, 15, 8, 142409)
    >>>
    >>> rtc.datetime((2018, 11, 18, 6, 12, 15, 5, 607409))
    (2018, 11, 18, 6, 12, 15, 8, 142409)


虽然RTC能够为我们进行时间和日期的跟踪，但是RTC的精度存在一定的缺陷，每过7:45h便会有秒级别的误差溢出，所以建议每隔7小时进行一次时间的校准。

由于计时器无法在掉电后进行计时工作，这就会导致你的设备在下次开机前进入初始的时间2000年1月1号。所以如果要对时间进行精准的掌控，我们需要在开机时进行时间的校准。
你可以使用 :mod:`ntptime` 模块进行网络授时校准时间。