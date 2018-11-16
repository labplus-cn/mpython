数字IO
===============

本章节介绍了I/O引脚的数字输入输出。掌控板可以通过拓展板将IO引脚拓展并连接控制或读取其他元器件或模块。

创建引脚对象::

    >>> from mpython import *
    >>> p0=MPythonPin(0,PinMode.IN)  
    
.. Note::

    使用前，请务必先将 ``mpython`` 模块 ``MPythonPin`` 导入，方可使用。“0”是您要访问的引脚。如果未指定mode，则默认为PinMode.IN
    

读数字输入
------------------    
    
使用读数字输入::

    >>> p0.read_digital()
    0
    >>> p0.read_digital()
    1

.. Note::

    返回引脚电平值。高电平(1),低电平(0)。


写数字输出
------------------    

将引脚并配置为输出模式::

    >>> p0=MPythonPin(0,PinMode.OUT)  

.. Hint::

    ``PinMode.OUT`` 为输出模式

对引脚写高低电平::

    >>> p0.write_digital(1)
    >>> p0.write_digital(0)


外部中断
-------------------

当输入引脚发生电平变化时触发硬件中断，触发器会执行中断处理函数。你可以定义回调函数来做中些断响应的工作。


让我们首先定义一个回调函数，它必须采用一个参数，``p`` 是触发函数的引脚号。我们将使该功能打印引脚：

    >>> def callback(p):
    ...     print('pin change', p)

接下来，我们将创建两个引脚并将它们配置为输入::

    >>> from mpython import *
    >>> p0 = MPythonPin(0,PinMode.IN)  
    >>> p1 = MPythonPin(0,PinMode.IN)  

最后我们需要告诉引脚何时触发，以及在检测到事件时调用的函数::

    >>> p0.irq(trigger=Pin.IRQ_FALLING, handler=callback)
    >>> p1.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=callback)

.. Note::

    我们将p0设置为仅在下降沿触发 ``Pin.IRQ_FALLING``（当它从高电平变为低电平时），并将通过or运算设置trigger在上升沿和下降沿触发。设置回调函数
    handler="你定义中断处理的回调函数"。输入此代码后，您可以向引脚0和1施加高电压和低电压，以查看正在执行的中断。更详细的中断方法，请查阅 :ref:`machine.irq <Pin.irq>` 。

事件发生后，硬中断将立即触发，并将中断任何正在运行的代码，包括Python代码。
因此，您的回调函数受限于它们可以执行的操作（例如，它们无法分配内存），并且应尽可能简短。

