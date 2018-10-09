Buttons
======================================

在掌控板上部边沿有按压式A、B两个按键。当按下按键时为低电平，否则高电平。除此外还有5个金手指触摸按键。


按键A、B
-------

使用前，导入mpython模块::

  >>> from mpython import *
  >>> 

你可以尝试下分别读取a按键 **按下** 和 **未按下** 两种状态的值::

  >>> button_a.value()       #读取按键a不按时的值
  1
  >>> button_a.value()       #读取按键a按下时的值
  0
 
.. Note::

  ``button_a`` 为按键a对象名，按键b对象名为 ``button_b`` 。是 ``machine.Pin`` 衍生类，继承Pin的方法。所以可使用 ``value`` 函数读取引脚值。
  返回 ``1`` 代表高电平信号，返回 ``0`` 代表低电平信号。


还可以使用引脚的中断处理，如当按下按键a,打印输出::
  
  >>> def callback(_):            #先定义中断处理函数
  ...     print('Button a Pressed')
  ... 
  >>> button_a.irq(trigger=Pin.IRQ_FALLING, handler=callback)     #设置按键a中断,下降沿触发
  >>> 

可以尝试按下按键a，看下中断效果。当检测到按键按下，回调打印::

    >>> Button Pressed
  Button Pressed
  Button Pressed
  Button Pressed
  Button Pressed

.. Note::

  定义中断处理函数时，函数必须包含任意一个参数，否则无法使用。callback()函数中的参数为 ``_`` 。
  ``trigger`` 可修改触发方式，``handler`` 为中断处理函数。详细使用可查阅  :ref:`Pin.irq<Pin.irq>`。



触摸按键
-------

首先导入TouchPad,Pin模块，构建TouchPad对象。此处我们使用掌控板触摸引脚Y，对应的ESP32的物理引脚为IO14。其他的引脚定义可参见 :ref:`掌控板引脚定义<mpython_pinout>` ::

  >>> from machine import TouchPad,Pin
  >>> Pad_Y = TouchPad(Pin(14))
  
尝试用手指触摸Y金手指处，使用 ``read()`` 读取值。观察变化::

  >>> Pad_Y.read()
  643
  >>> Pad_Y.read()
  8