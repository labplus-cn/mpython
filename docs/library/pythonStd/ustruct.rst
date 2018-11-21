:mod:`ustruct` -- 打包和解压缩原始数据类型
======================================================

.. module:: ustruct
   :synopsis: 打包和解压缩原始数据类型

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `struct <https://docs.python.org/3.5/library/struct.html#module-struct>`_


支持的大小/字节顺序前缀: ``@``, ``<``, ``>``, ``!``.

支持的格式编码: ``b``, ``B``, ``h``, ``H``, ``i``, ``I``, ``l``,
``L``, ``q``, ``Q``, ``s``, ``P``, ``f``, ``d`` 后两个取决于浮点支持）。

函数
---------

.. function:: calcsize(fmt)

   返回需存入给定 *fmt* 的字节数量。

.. function:: pack(fmt, v1, v2, ...)

   根据格式字符串fmt，打包 *v1, v2, ...* 值。返回值为一个解码该值的字节对象。

.. function:: pack_into(fmt, buffer, offset, v1, v2, ...)

   根据格式字符串fmt，将 *v1, v2, ...* 值打包进从 *offset* 开始的缓冲区。从缓冲区的末端计数， *offset* 可能为负值。

.. function:: unpack(fmt, data)

   根据格式字符串 *fmt* 对数据进行解压。返回值为一个解压值元组。

.. function:: unpack_from(fmt, data, offset=0)

   根据格式字符串 *fmt* 解压从 *offset* 开始的数据。从缓冲区的末端计数， *offset* 可能为负值。返回值是一个解压值元组。