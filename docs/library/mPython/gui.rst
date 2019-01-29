.. _gui:
:mod:`gui`

gui 模块
==========


.. class:: UI

UI类
-------

提供UI界面类控件

.. class:: UI(oled)

构建UI对象。

    - ``oled``  - 传入framebuf类的对象,如是mPython OLED显示屏,则oled对象。

.. method:: UI.ProgressBar(x, y, width, height, progress)

绘制进度条。

    - ``x`` 、 ``y`` -左上角作为起点坐标
    - ``width`` -进度条宽度
    - ``height`` -进度条高度
    - ``progress`` -进度条百分比

::

    from mpython import *

    myUI=UI(oled)
    myUI.ProgressBar(30,30,70,8,60)
    oled.show()

.. method:: UI.stripBar(x, y, width, height, progress,dir=1,frame=1)

绘制垂直或水平的柱状条

    - ``x`` 、 ``y`` -左上角作为起点坐标
    - ``width`` -柱状条宽度
    - ``height`` -柱状条高度
    - ``progress`` -柱状条百分比
    - ``dir`` -柱状条方向。dir=1时水平方向,dir=0时,垂直方向。
    - ``frame`` -当frame=1时,显示外框；当frame=0时,不显示外框。

Clock类
+++++

提供模拟钟表显示功能

.. class:: Clock(oled,x,y,radius)

构建Clock对象。

    - ``oled``  - 传入framebuf类的对象,如是mPython OLED显示屏,则oled对象。
    - ``x`` 、``y`` -左上角作为起点坐标
    - ``radius`` -钟表半径


.. method:: settime()

获取本地时间并设置模拟钟表时间


.. method:: drawClock()

绘制钟表

.. method:: clear()

清除钟表

::

    from mpython import*
    from machine import Timer
    import time


    clock=Clock(oled,64,32,30)

    def Refresh():
            clock.settime()
            clock.drawClock()
            oled.show()
            clock.clear()

    tim1 = Timer(1)

    tim1.init(period=1000, mode=Timer.PERIODIC, callback=lambda _:Refresh())
