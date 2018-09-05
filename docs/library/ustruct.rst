:mod:`ustruct` -- pack and unpack primitive data types
======================================================

.. module:: ustruct
   :synopsis: pack and unpack primitive data types

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `struct <https://docs.python.org/3.5/library/struct.html#module-struct>`_

Supported size/byte order prefixes: ``@``, ``<``, ``>``, ``!``.

Supported format codes: ``b``, ``B``, ``h``, ``H``, ``i``, ``I``, ``l``,
``L``, ``q``, ``Q``, ``s``, ``P``, ``f``, ``d`` (the latter 2 depending
on the floating-point support).

Functions
---------

.. function:: calcsize(fmt)

   Return the number of bytes needed to store the given *fmt*.

.. function:: pack(fmt, v1, v2, ...)

   Pack the values *v1*, *v2*, ... according to the format string *fmt*.
   The return value is a bytes object encoding the values.

.. function:: pack_into(fmt, buffer, offset, v1, v2, ...)

   Pack the values *v1*, *v2*, ... according to the format string *fmt*
   into a *buffer* starting at *offset*. *offset* may be negative to count
   from the end of *buffer*.

.. function:: unpack(fmt, data)

   Unpack from the *data* according to the format string *fmt*.
   The return value is a tuple of the unpacked values.

.. function:: unpack_from(fmt, data, offset=0)

   Unpack from the *data* starting at *offset* according to the format string
   *fmt*. *offset* may be negative to count from the end of *buffer*. The return
   value is a tuple of the unpacked values.
