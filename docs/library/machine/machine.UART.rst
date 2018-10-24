.. currentmodule:: machine
.. _machine.UART:

类 UART -- 双工串行通信总线
=============================================

UART实现标准UART / USART双工串行通信协议。在物理层面，它由2根线组成：RX和TX。
通信单元是一个字符（不要与字符串混淆），可以是8bit或9bit宽。

可以使用以下命令创建和初始化UART对象::

    from machine import UART

    uart = UART(1, 9600)                         # init with given baudrate
    uart.init(9600, bits=8, parity=None, stop=1) # init with given parameters

UART对象就像一个 ``stream`` 对象，使用标准流方法完成读写::

    uart.read(10)       # read 10 characters, returns a bytes object
    uart.read()         # read all available characters
    uart.readline()     # read a line
    uart.readinto(buf)  # read and store into the given buffer
    uart.write('abc')   # write the 3 characters

构建对象
------------

.. class:: UART(id, ...)

   构造给定id的UART对象

方法
-------



.. method:: UART.init(baudrate=9600, bits=8, parity=None, stop=1, \*, pins=(TX, RX, RTS, CTS))

使用给定参数初始化UART总线:

    - ``baudrate`` 时钟频率
    - ``bits`` 每个字符的位数，7,8或9
    - ``parity`` 奇偶校验是奇偶校验， ``None`` 0（偶数）或1（奇数）
    - ``stop`` 停止位的数量，1或2
    - ``pins`` 一个4或2项列表，指示TX、RX、RTS和CTS引脚(按该顺序)。如果想让UART在功能有限的情况下运行，任何一个引脚都可以是空的。如果RTS引脚是给定的，那么RX引脚也必须给定。CTS也是如此。如果没有引脚，则获取TX和RX引脚的默认设置，以及硬件流量控制将被禁用。如果pins=None，则不会进行pin赋值。

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

   发送中断条件在总线上。使总线驱动的持续时间长于正常传输字符所需的持续时间。



.. method:: UART.irq(trigger, priority=1, handler=None, wake=machine.IDLE)

   创建一个回调，以便在UART上接收数据时触发。

        - ``trigger`` 只能是 ``UART.RX_ANY``
        - ``priority`` 可以取1-7范围内的值。值越高表示优先级越高。
        - ``handler`` 当新字符到达时要调用的可选函数
        - ``wake`` 只能是 ``machine.IDLE``.

    .. note::

        当满足以下两个条件之一时，将调用handler:

            - 已经接收到8个新字符。
            - 在Rx缓冲区中至少有一个新字符正在等待，并且Rx在1个完整帧的持续时间内一直处于静默状态。

       这意味着当调用处理函数时，将有1到8个字符在等待。

    返回一个irq对象。


常数
---------

.. data:: UART.RX_ANY


    IRQ触发源

