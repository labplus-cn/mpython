:mod:`esp` --- ESP32相关的功能
=========================================================

.. module:: esp
    :synopsis: ESP32相关的功能


该 ``esp`` 模块包含ESP32模块相关的特定功能。


函数
---------

.. function:: flash_size()

    返回flash的大小。

.. function:: flash_user_start()

    读取用户flash空间开始的内存偏移量。

.. function:: flash_read(byte_offset, length_or_buffer)

    从地址为 byte_offset 的 flash 起始点读取 buf.len()个长度的数据并放入 buf 中。

    - ``byte_offset`` ：flash偏移地址
    - ``buf`` ：接收数据缓冲区，缓冲区的长度为len

    ::

        import esp

        buf = bytearray(100)
        esp.flash_read(2097152, buf)

.. function:: flash_write(byte_offset, bytes)

    将 buf 中所有的数据写入地址为 byte_offset 的 flash 区域。

    - ``byte_offset`` ：flash偏移地址
    - ``buf`` ：数据缓冲区，缓冲区长度为len

    ::

        buf = bytearray(100)
        esp.flash_write(2097152, buf)

.. function:: flash_erase(sector_no)

    擦除flash扇区

    - ``ector_no`` :要擦除的扇区

    ::

        esp.flash_erase(512)

.. function:: osdebug()
