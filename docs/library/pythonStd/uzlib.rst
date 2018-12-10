:mod:`uzlib` -- zlib解压缩
==================================

.. module:: uzlib
   :synopsis: zlib decompression

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `zlib <https://docs.python.org/3.5/library/zlib.html#module-zlib>`_

该模块允许解压用DEFLATE算法（常用于zlib库和gzip压缩程式）压缩的二进制数据。压缩尚未实现。

函数
---------

.. function:: decompress(data, wbits=0, bufsize=0)

   将解压缩数据返回为字节。 *wbits* 是压缩时使用的DEFLATE字典窗口大小（8-15，字典的大小为该数值的2次幂）。
   另外，若该值为正， *data* 则被假定为zlib流（带有zlib首标）。否则，若该值为负，
   则假定为原始DEFLATE流。 *bufsize* 参数是为与CPython兼容，此处忽略。

.. class:: DecompIO(stream, wbits=0)

   创建一个流装饰器，该装饰器允许在另一个流中进行压缩数据的透明解压。
   这允许使用大于可用堆大小的数据处理压缩流。除 `decompress()` 中所述的值外， *wbits* 可能取值24..31 (16 + 8..15)，这也就意味着输入流带有gzip首标。

   .. admonition:: 与CPython区别
      :class: attention

      该类为MicroPython的扩展，暂时使用该类，在后续版本中可能会进行较大的修改或删除。