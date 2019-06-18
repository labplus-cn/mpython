.. currentmodule:: machine
.. _machine.UART:

类 UART -- 双工串行通信总线
=============================================

UART实现标准UART / USART双工串行通信协议。在物理层面，它由2根线组成：RX和TX。
通信单元是一个字符（不要与字符串混淆），可以是8bit或9bit宽。


构建对象
------------

.. class:: UART(id, ...)

    构造UART对象

    - ``id`` - 串口号:1、2  

    .. Attention:: 
    
    ``UART(id=0)`` 用于REPL,不能使用！

    ::
    
        from machine import UART
        from machine import Pin

        uart = UART(1, baudrate=115200, rx=Pin.P15, tx=Pin.P16, timeout=10)

方法
-------

.. method:: UART.init(baudrate=9600, bits=8, parity=None, stop=1, \*, ...)

使用给定参数初始化UART总线


    - ``baudrate`` - 波特率
    - ``bits``- 每个字符的位数，7,8或9。
    - ``parity``- 奇偶校验:0-偶数,1-奇数
    - ``rx`` , ``tx`` - UART读、写引脚
    - ``stop`` - 停止位数量:1、2
    - ``timeout``- 超时时间（单位：毫秒） < timeout ≤ 0x7FFF FFFF (十进制：0 < timeout ≤ 2147483647)
    - ``txbuf`` - 指定TX缓冲区的字符长度
    - ``rxbuf`` - 指定RX缓冲区的字符长度

    .. Attention:: 

        * 所有引脚均可以作为串口的输入RX，除 ``P2``、``P3`` 、``P4`` 、``P10`` 只能作为输入，其余所有的引脚理论上都可以作为输出TX。
        * ``GPIO 1`` 、``GPIO 3`` 用于掌控板的USB串口，在初始化UART定义 ``tx`` ，``rx`` 引脚一般不使用，除非你要用到掌控板的USB接口作为串口输出。





.. method:: UART.deinit()

   关闭UART总线。

.. method:: UART.any()

    返回一个整数，计算可以无阻塞地读取的字符数。如果没有可用字符，它将返回0，如果有字符，则返回正数。
    即使有多个可读的字符，该方法也可以返回1。

   要查询更复杂的可用字符，请使用select.poll::

    poll = select.poll()
    poll.register(uart, select.POLLIN)
    poll.poll(timeout)

.. method:: UART.read([nbytes])

    读字符。如果 ``nbytes`` 指定，则最多读取多个字节，否则读取尽可能多的数据。

    返回值：包含读入的字节的字节对象。 ``None`` 超时时返回。

.. method:: UART.readinto(buf[, nbytes])

   将字节读入 ``buf`` 。如果 ``nbytes`` 指定，则最多读取多个字节。否则，最多读取 ``len(buf)`` 字节数。

   返回值：读取和存储到超时 ``buf`` 或 ``None`` 超时的字节数。

.. method:: UART.readline()

   读一行，以换行符结尾。

   返回值：读取行或 ``None`` 超时。

.. method:: UART.write(buf)

   将字节缓冲区写入总线。

   返回值：写入或 ``None`` 超时的字节数。

.. method:: UART.sendbreak()

   在总线上发送中断。这使总线驱动的持续时间长于正常传输字符所需的时间。