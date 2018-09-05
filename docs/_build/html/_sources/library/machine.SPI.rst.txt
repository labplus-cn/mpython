.. currentmodule:: machine
.. _machine.SPI:

类 SPI -- 串行外设接口总线协议 (主端)
=====================================================================

SPI是由主设备驱动的同步串行协议。在物理层面，总线由3条线组成：SCK，MOSI，MISO。
多个设备可以共享同一总线。每个设备都应有一个单独的第4个信号SS（从选择），用于选择与之进行通信的总线上的特定设备。
SS信号的管理应该在用户代码中进行（通过 :class:`machine.Pin` 类）。

构建函数
------------

.. class:: SPI(id, ...)

在给定总线上构造SPI对象，``id`` 值依赖于特定的端口及其硬件。
值0是、1等通常用于选择硬件SPI块#0、#1等。值是-1可以用于SPI的bitsmashing(软件)实现(如果由一个端口支持的话)。

如果没有其他参数，则会创建SPI对象但不进行初始化（它具有上次初始化总线的设置，如果有的话）。
如果给出额外的参数，则初始化总线。请参阅 ``init`` 初始化参数。

方法
-------

.. method:: SPI.init(baudrate=1000000, \*, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=None, mosi=None, miso=None, pins=(SCK, MOSI, MISO))

   Initialise the SPI bus with the given parameters:

     - ``baudrate`` is the SCK clock rate.
     - ``polarity`` can be 0 or 1, and is the level the idle clock line sits at.
     - ``phase`` can be 0 or 1 to sample data on the first or second clock edge
       respectively.
     - ``bits`` is the width in bits of each transfer. Only 8 is guaranteed to be supported by all hardware.
     - ``firstbit`` can be ``SPI.MSB`` or ``SPI.LSB``.
     - ``sck``, ``mosi``, ``miso`` are pins (machine.Pin) objects to use for bus signals. For most
       hardware SPI blocks (as selected by ``id`` parameter to the constructor), pins are fixed
       and cannot be changed. In some cases, hardware blocks allow 2-3 alternative pin sets for
       a hardware SPI block. Arbitrary pin assignments are possible only for a bitbanging SPI driver
       (``id`` = -1).
     - ``pins`` - WiPy port doesn't ``sck``, ``mosi``, ``miso`` arguments, and instead allows to
       specify them as a tuple of ``pins`` parameter.

.. method:: SPI.deinit()

   Turn off the SPI bus.

.. method:: SPI.read(nbytes, write=0x00)

    Read a number of bytes specified by ``nbytes`` while continuously writing
    the single byte given by ``write``.
    Returns a ``bytes`` object with the data that was read.

.. method:: SPI.readinto(buf, write=0x00)

    Read into the buffer specified by ``buf`` while continuously writing the
    single byte given by ``write``.
    Returns ``None``.

    Note: on WiPy this function returns the number of bytes read.

.. method:: SPI.write(buf)

    Write the bytes contained in ``buf``.
    Returns ``None``.

    Note: on WiPy this function returns the number of bytes written.

.. method:: SPI.write_readinto(write_buf, read_buf)

    Write the bytes from ``write_buf`` while reading into ``read_buf``.  The
    buffers can be the same or different, but both buffers must have the
    same length.
    Returns ``None``.

    Note: on WiPy this function returns the number of bytes written.

Constants
---------

.. data:: SPI.MASTER

   for initialising the SPI bus to master; this is only used for the WiPy

.. data:: SPI.MSB

   set the first bit to be the most significant bit

.. data:: SPI.LSB

   set the first bit to be the least significant bit
