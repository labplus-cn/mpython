:mod:`uctypes` -- 以结构化方式访问二进制数据
========================================================

.. module:: uctypes
   :synopsis: 以结构化方式访问二进制数据

该模块为MicroPython实现“外部数据接口”。它背后的想法类似于CPython的 ``ctypes`` 模块，但实际的API是不同的，
简化并针对小尺寸进行了优化。该模块的基本思想是定义具有与C语言允许的功能大致相同的数据的数据结构布局，
然后使用熟悉的点语法访问它以引用子字段。

.. 也可以看看 ::

    Module :mod:`ustruct`
        用于访问二进制数据结构的标准Python方法（不能很好地扩展到大型和复杂的结构）。


构建对象
------------

.. class:: uctypes.struct(addr, descriptor, type) 

将内存中以c形式打包的结构体或联合体转换为字典，并返回该字典。

- ``addr``:开始转换的地址
- ``descriptor``:转换描述符

  -  ``格式``: "field_name":offset|uctypes.UINT32
  -  ``offset``：偏移量，单位：字节,  VOID、UINT8、INT8、UINT16、INT16、UINT32、INT32、UINT64、INT64、BFUINT8、BFINT8、BFUINT16、BFINT16、BFUINT32、BFINT32、BF_POS、BF_LEN、FLOAT32、FLOAT64、PTR、ARRAY
- ``type``:c结构体或联合体存储类型，默认为本地存储类型

  - ``NATIVE``:MricoPython本地的存储类型
  - ``LITTLE_ENDIAN``:小端存储
  - ``BIG_ENDIAN``:大端存储 

示例::

  #如果需要C文件中的结构体，需要使用VC或者VS生成.dll（windows）或.os（linux、mac）文件，然后下载进入MCU中，使用MCU打开此文件，获取结构体或联合体
  >>> a = b"0123"
  >>> s = uctypes.struct(uctypes.addressof(a), {"a": uctypes.UINT8 | 0, "b": uctypes.UINT16 | 1}, uctypes.LITTLE_ENDIAN)
  >>> print(s)
  <struct STRUCT 3ffc7360>
  >>> print(s.a)
  48
  >>> s.a = 49
  >>> print(a)
  b'1123'