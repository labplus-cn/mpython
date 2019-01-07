.. currentmodule:: machine
.. _machine.WDT:

类 WDT -- 看门狗定时器
===========================

当程序崩溃并最终进入不可恢复状态时，WDT用于重新启动系统。一旦启动，就无法以任何方式停止或重新配置。
启用后，程序必须定期 ``喂狗`` ，以防止它过期和重置系统。

示例::

    from machine import WDT
    wdt = WDT()        # enable it with a wdt
    wdt.feed()


构建对象
------------

.. class:: WDT()

  创建一个WDT对象并启动它。

方法
-------

.. method:: wdt.feed()

  对WDT喂狗以防止它重置系统。程序应该将此调用放置在一个合理的位置，以确保在验证所有操作都正确之后才会对WDT进行喂狗。
