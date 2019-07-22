.. _gui:

.. module:: gui
   :synopsis: 提供GUI类的绘制的相关功能函数

:mod:`gui` --- 提供GUI类的绘制的相关功能函数
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

.. method:: UI.qr_code(str,x,y,scale=2)

    绘制29*29二维码

    - ``str`` - 二维码数据,类型字符串
    - ``x`` 、 ``y`` -左上角作为起点坐标
    - ``scale`` -放大倍数:可以为1,2。默认为2倍放大。

::

    import gui
    from mpython import *
    ui=gui.UI(oled)
    ui.qr_code('https://mpython.readthedocs.io',0,0)
    oled.show()

Clock类
+++++++++

提供模拟钟表显示功能

.. class:: Clock(oled,x,y,radius)

构建Clock对象。

    - ``oled``  - 传入framebuf类的对象,如是mPython OLED显示屏,则oled对象。
    - ``x`` 、``y`` -左上角作为起点坐标
    - ``radius`` -钟表半径


.. method:: Clock.settime()

获取本地时间并设置模拟钟表时间


.. method:: Clock.drawClock()

绘制钟表

.. method:: Clock.clear()

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



Image
+++++++++

支持 `pbm` 和 `bmp` 1bit的图片格式。

.. Class:: Image()

构建Image对象

.. method:: Image.load(path, invert=0)


加载 `pbm` 或 `bmp` 图片格式文件,返回该图片的 :class:`framebuf.FrameBuffer` 对象。   

- ``path`` - 图片文件路径
- ``invert`` - 像素点反转。0表示不反转,1则反转。


示例::

    from mpython import *
    from gui import Image

    image = Image()
    fb = image.load('clown_1.bmp',1 )

    oled.blit(fb, 0, 0)
    oled.show()
