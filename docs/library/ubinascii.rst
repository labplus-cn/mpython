:mod:`ubinascii` -- 二进制/ ASCII转换
============================================

.. module:: ubinascii
   :synopsis: 二进制/ ASCII转换

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `binascii <https://docs.python.org/3.5/library/binascii.html#module-binascii>`_

该模块实现了二进制数据与各种ASCII编码之间的转换(双向).

Functions
---------

.. function:: hexlify(data, [sep])

   Convert binary data to hexadecimal representation. Returns bytes string.

   .. admonition:: Difference to CPython
      :class: attention

      If additional argument, *sep* is supplied, it is used as a separator
      between hexadecimal values.

.. function:: unhexlify(data)

   Convert hexadecimal data to binary representation. Returns bytes string.
   (i.e. inverse of hexlify)

.. function:: a2b_base64(data)

   Decode base64-encoded data, ignoring invalid characters in the input.
   Conforms to `RFC 2045 s.6.8 <https://tools.ietf.org/html/rfc2045#section-6.8>`_.
   Returns a bytes object.

.. function:: b2a_base64(data)

   Encode binary data in base64 format, as in `RFC 3548
   <https://tools.ietf.org/html/rfc3548.html>`_. Returns the encoded data
   followed by a newline character, as a bytes object.
