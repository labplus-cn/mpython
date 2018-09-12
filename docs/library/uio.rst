:mod:`uio` -- 输入/输出流
==================================

.. module:: uio
   :synopsis: 输入/输出流

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `io <https://docs.python.org/3.5/library/io.html#module-io>`_

此模块包含其他类型的stream（类文件）对象和帮助程序函数。

概念层次
--------------------

.. admonition:: 与CPython的区别
   :class: attention

   如本节所述，MicroPython中简化了流基类的概念层次结构。

(Abstract) base stream classes, which serve as a foundation for behavior
of all the concrete classes, adhere to few dichotomies (pair-wise
classifications) in CPython. In MicroPython, they are somewhat simplified
and made implicit to achieve higher efficiencies and save resources.

An important dichotomy in CPython is unbuffered vs buffered streams. In
MicroPython, all streams are currently unbuffered. This is because all
modern OSes, and even many RTOSes and filesystem drivers already perform
buffering on their side. Adding another layer of buffering is counter-
productive (an issue known as "bufferbloat") and takes precious memory.
Note that there still cases where buffering may be useful, so we may
introduce optional buffering support at a later time.

But in CPython, another important dichotomy is tied with "bufferedness" -
it's whether a stream may incur short read/writes or not. A short read
is when a user asks e.g. 10 bytes from a stream, but gets less, similarly
for writes. In CPython, unbuffered streams are automatically short
operation susceptible, while buffered are guarantee against them. The
no short read/writes is an important trait, as it allows to develop
more concise and efficient programs - something which is highly desirable
for MicroPython. So, while MicroPython doesn't support buffered streams,
it still provides for no-short-operations streams. Whether there will
be short operations or not depends on each particular class' needs, but
developers are strongly advised to favor no-short-operations behavior
for the reasons stated above. For example, MicroPython sockets are
guaranteed to avoid short read/writes. Actually, at this time, there is
no example of a short-operations stream class in the core, and one would
be a port-specific class, where such a need is governed by hardware
peculiarities.

The no-short-operations behavior gets tricky in case of non-blocking
streams, blocking vs non-blocking behavior being another CPython dichotomy,
fully supported by MicroPython. Non-blocking streams never wait for
data either to arrive or be written - they read/write whatever possible,
or signal lack of data (or ability to write data). Clearly, this conflicts
with "no-short-operations" policy, and indeed, a case of non-blocking
buffered (and this no-short-ops) streams is convoluted in CPython - in
some places, such combination is prohibited, in some it's undefined or
just not documented, in some cases it raises verbose exceptions. The
matter is much simpler in MicroPython: non-blocking stream are important
for efficient asynchronous operations, so this property prevails on
the "no-short-ops" one. So, while blocking streams will avoid short
reads/writes whenever possible (the only case to get a short read is
if end of file is reached, or in case of error (but errors don't
return short data, but raise exceptions)), non-blocking streams may
produce short data to avoid blocking the operation.

The final dichotomy is binary vs text streams. MicroPython of course
supports these, but while in CPython text streams are inherently
buffered, they aren't in MicroPython. (Indeed, that's one of the cases
for which we may introduce buffering support.)

Note that for efficiency, MicroPython doesn't provide abstract base
classes corresponding to the hierarchy above, and it's not possible
to implement, or subclass, a stream class in pure Python.

函数
---------

.. function:: open(name, mode='r', **kwargs)

   打开一个文件。内置open()函数是此函数的别名。

类
-------

.. class:: FileIO(...)

    这是以二进制模式打开的文件类型，例如使用 ``open(name, "rb")`` 
    您不应该直接实例化这个类。

.. class:: TextIOWrapper(...)

    这是在文本模式下打开的文件类型，例如使用 ``open(name, "rt")`` 。
    您不应该直接实例化这个类。

.. class:: StringIO([string])

.. class:: BytesIO([string])


    用于输入/输出的内存文件类对象。 ``StringIO`` 用于文本模式I / O（类似于使用“t”修饰符打开的普通文件）。``BytesIO`` 用于二进制模式I ​​/ O（类似于使用“b”修饰符打开的普通文件）。可以使用字符串参数指定类文件对象的初始内容（应为普通字符串StringIO或字节对象BytesIO）。
    所有常见的文件的方法，如 ``read()`` ， ``write()`` ， ``seek()`` ， ``flush()`` ， ``close()``  在这些对象上可用以下的方法:


    .. method:: getvalue()

       获取保存数据的底层缓冲区的当前内容。
