.. currentmodule:: machine
.. _machine.SPI:

类 SPI -- 串行外设接口总线协议 (主端)
=====================================================================

SPI是由主设备驱动的同步串行协议。在物理层面，总线由3条线组成：SCK，MOSI，MISO。
多个设备可以共享同一总线。每个设备都应有一个单独的第4个信号SS（从选择），用于选择与之进行通信的总线上的特定设备。
SS信号的管理应该在用户代码中进行（通过 :class:`machine.Pin` 类）。

构建对象
------------

.. class:: SPI(id, ...)

在给定总线上构造SPI对象，``id`` 值依赖于特定的端口及其硬件。
值0是、1等通常用于选择硬件SPI块#0、#1等。值是-1可以用于SPI的bitsmashing(软件)实现(如果由一个端口支持的话)。

如果没有其他参数，则会创建SPI对象但不进行初始化（它具有上次初始化总线的设置，如果有的话）。
如果给出额外的参数，则初始化总线。请参阅 ``init`` 初始化参数。

方法
-------

.. method:: SPI.init(baudrate=1000000, \*, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=None, mosi=None, miso=None, pins=(SCK, MOSI, MISO))

   使用给定参数初始化SPI总线：

     - ``baudrate`` SCK时钟频率。
     - ``polarity`` 0或1，空闲时钟线所在的电平。
     - ``phase`` 0或1来分别在第一或第二时钟边沿上采样数据。
     - ``bits`` 每次传输的宽度（以位为单位）。所有硬件都保证只支持8个。
     - ``firstbit`` 可以是  ``SPI.MSB`` 或 ``SPI.LSB``.
     - ``sck``, ``mosi``, ``miso`` 是 pins (machine.Pin) 对象以用于总线信号。对于大多数硬件SPI块（由 ``id`` 构建对象的参数选择），引脚是固定的，不能更改。在某些情况下，硬件模块允许2-3个替代引脚组用于硬件SPI模块。任意引脚分配仅适用于bitbanging SPI驱动程序（ ``id`` = -1）。
     - ``pins`` -  esp32没有 ``sck`` ， ``mosi`` ， ``miso`` 参数，而是允许指定它们作为一个元组 ``pins`` 参数。

.. method:: SPI.deinit()

   关闭SPI总线。

.. method:: SPI.read(nbytes, write=0x00)

   读取指定的字节数， ``nbytes`` 同时连续写入由给定的单字节 ``write`` 。返回包含 ``bytes`` 已读取数据的对象。

.. method:: SPI.readinto(buf, write=0x00)

    读入 ``buf`` 指定的缓冲区，同时不断写入由 ``write`` 给出的单字节。

    返回 ``None``。

    注意：在 ``esp32`` 上，此函数返回读取的字节数。


.. method:: SPI.write(buf)

    写入`` buf`` 中的字节。

    返回 ``None``。

    注意：：在 ``esp32`` 上，此函数返回写入的字节数。

.. method:: SPI.write_readinto(write_buf, read_buf)

    从 ``write_buf`` 中写入字节，同时读入 ``read_buf`` 中。缓冲区可以是相同的，也可以是不同的，但是两个缓冲区都必须具有
    长度相同。

    返回 ``None``。

    注意：在 ``esp32`` 上，此函数返回写入的字节数。

常数
---------

.. data:: SPI.MASTER

   用于初始化SPI总线到主机; 这仅用于 ``esp32``。

.. data:: SPI.MSB

   将第一位设置为最高位。

.. data:: SPI.LSB

   将第一个位设置为最低位。
