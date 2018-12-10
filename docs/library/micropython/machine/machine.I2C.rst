.. currentmodule:: machine
.. _machine.I2C:

类 I2C --  双线串行协议
=======================================

I2C是用于设备之间通信的双线协议。在物理层面，它由2条线组成：SCL和SDA，分别是时钟和数据线。

创建连接到特定总线的I2C对象。它们可以在创建时初始化，也可以在以后初始化。

示例::

        from machine import I2C,Pin

        i2c = I2C(scl=Pin(22), sda=Pin(23), freq=400000)          # create I2C peripheral at frequency of 400kHz
                                                                                                                                                                                                                                                # depending on the port, extra parameters may be required
                                                                                                                                                                                                                                                # to select the peripheral and/or pins to use

        i2c.scan()                      # scan for slaves, returning a list of 7-bit addresses

        i2c.writeto(42, b'123')         # write 3 bytes to slave with 7-bit address 42
        i2c.readfrom(42, 4)             # read 4 bytes from slave with 7-bit address 42

        i2c.readfrom_mem(42, 8, 3)      # read 3 bytes from memory of slave 42,
                                                                                                                                        #   starting at memory-address 8 in the slave
        i2c.writeto_mem(42, 2, b'\x10') # write 1 byte to memory of slave 42
                                                                                                                                        #   starting at address 2 in the slave
构建对象
------------

.. class:: I2C(id=-1, \*, scl, sda, freq=400000)

   使用以下参数构造并返回新的I2C对象：
        


        - ``id`` 标识特定的I2C外设。默认值-1选择I2C的软件实现
        - ``scl`` 应该是一个pin对象，指定用于SCL的引脚
        - ``sda`` 应该是一个pin对象，指定用于SDA的引脚
        - ``freq`` 应该是一个整数，它设置SCL的最大频率。0 < freq ≤ 500000(Hz)。

.. Attention:: 

        I2C可使用引脚有GPIO 0/2/4/5/9/16/17/18/19/21/22/23/25/26/27

General Methods
---------------

.. method:: I2C.init(scl, sda, \*, freq=400000)

        Initialise the I2C bus with the given arguments:

     - ``scl`` 是SCL线的pin对象
     - ``sda`` 是SDA线的pin对象
     - ``freq`` 是SCL时钟速率

.. method:: I2C.deinit()

   关闭I2C总线。

.. method:: I2C.scan()

 扫描0x08和0x77之间的所有I2C地址，并返回响应的列表。如果在总线上发送其地址（包括写入位）后将器件拉低，则器件会响应。

Primitive I2C operations
------------------------

以下方法实现Primitive I2C operations主总线操作，并且可以组合以进行任何I2C事务。如果您需要更多控制总线，则提供它们，
否则可以使用标准方法（见下文）。

.. method:: I2C.start()

   在总线上生成START条件（SDA在SCL为高电平时转换为低电平）。

.. method:: I2C.stop()

        在总线上生成STOP条件（SDA在SCL为高电平时转换为高电平）。

.. method:: I2C.readinto(buf, nack=True)

从总线读取字节并将它们存储到 ``buf`` 中。读取的字节数是 ``buf`` 的长度。在接收到除最后一个字节之外的所有字节之后，
将在总线上发送 ``ACK`` 。在接收到最后一个字节之后，如果 ``nack``  为真，则将发送 ``NACK``，否则将发送  ``ACK`` （并且在这种情况下，从属设备假定在稍后的调用中将读取更多字节）。


.. method:: I2C.write(buf)

将 ``buf`` 中的字节写入总线。检查每个字节后是否收到 ``ACK`` ，如果收到 ``NACK`` ，则停止发送剩余的字节。该函数返回已接收的 ``ACK`` 数。


Standard bus operations
-----------------------

下面的方法实现了针对给定从设备的标准I2C主读写操作。

.. method:: I2C.readfrom(addr, nbytes, stop=True)

从 ``addr`` 指定的从程序中读取 ``nbytes`` 。如果  ``stop`` 为真，则在传输结束时生成一个停止条件。返回一个读取数据的 ``bytes`` 对象。

.. method:: I2C.readfrom_into(addr, buf, stop=True)

从 ``addr`` 指定的奴隶读入 ``buf`` 。读取的字节数将是 ``buf`` 的长度。如果 ``stop`` 为真，则在传输结束时生成一个停止条件。

该方法返回 ``None`` 。
  

.. method:: I2C.writeto(addr, buf, stop=True)

将 ``buf`` 中的字节写入 ``addr`` 指定的从机。如果在从 ``buf`` 写入一个字节后收到 NACK  ，则不发送剩余的字节。
如果 ``stop`` 为true，则即使收到NACK，也会在传输结束时生成STOP条件。该函数返回已接收的ACK数。


寄存器操作
-----------------

某些I2C器件充当可以读写的存储器器件（或寄存器集）。在这种情况下，有两个与I2C事务相关的地址：从地址和存储器地址。
以下方法是与这些设备通信的便利功能。

.. method:: I2C.readfrom_mem(addr, memaddr, nbytes, \*, addrsize=8)

从 ``memaddr`` 指定的内存地址开始，从 ``addr`` 指定的slave中读取 ``nbytes`` 。参数 ``addrsize`` 以位为单位指定地址大小。
返回读取数据的 ``bytes`` 对象。

.. method:: I2C.readfrom_mem_into(addr, memaddr, buf, \*, addrsize=8)
    
从 ``memaddr`` 指定的内存地址开始，从 ``addr`` 指定的slave中读入 ``buf`` 。读取的字节数是 ``buf`` 的长度。
参数 ``addrsize`` 以位为单位指定地址大小。

该方法返回 ``None`` 。

.. method:: I2C.writeto_mem(addr, memaddr, buf, \*, addrsize=8)

从 ``memaddr`` 指定的内存地址开始，将 ``buf`` 写入 ``addr`` 指定的从机。参数 ``addrsize`` 以位的形式指定地址大小。

该方法返回 ``None`` 。
