:mod:`ubinascii` -- 二进制/ ASCII转换
============================================

.. module:: ubinascii
   :synopsis: 二进制/ ASCII转换

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `binascii <https://docs.python.org/3.5/library/binascii.html#module-binascii>`_

该模块实现了二进制数据与各种ASCII编码之间的转换(双向).

Functions
---------

.. function:: hexlify(data, [sep])

   将字符串转换为十六进制表示的字符串。 

   .. admonition:: 与CPython的区别
      :class: attention

      如果提供了附加参数sep，则它将用作十六进制值之间的分隔符。
   
   没有sep参数::

      >>> ubinascii.hexlify('\x11\x22123')
      b'1122313233'
      >>> ubinascii.hexlify('abcdfg')
      b'616263646667'
   
   如果指定了第二个参数sep，它将用于分隔两个十六进制数::

      >>> ubinascii.hexlify('\x11\x22123', ' ')
      b'11 22 31 32 33'
      >>> ubinascii.hexlify('\x11\x22123', ',')
      b'11,22,31,32,33'



.. function:: unhexlify(data)

   转换十六进制字符串为二进制字符串，功能和 hexlify 相反。

   示例::

      >>> ubinascii.unhexlify('313233')
      b'123'



.. function:: a2b_base64(data)

   解码base64编码的数据，忽略输入中的无效字符。符合  `RFC 2045 s.6.8 <https://tools.ietf.org/html/rfc2045#section-6.8>`_ 。返回一个 ``bytes`` 对象。


.. function:: b2a_base64(data)

   以base64格式编码二进制数据，如 `RFC 3548 <https://tools.ietf.org/html/rfc3548.html>`_ 中所述。返回编码数据，后跟换行符，作为 ``bytes`` 对象。

