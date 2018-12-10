:mod:`uhashlib` -- 散列算法
=====================================

.. module:: uhashlib
   :synopsis: 散列算法

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `hashlib <https://docs.python.org/3.5/library/hashlib.html#module-hashlib>`_

该模块实现二进制数据散列算法。可用算法的确切清单取决于board。在可以实现的算法中：

* SHA256 -  当前一代的现代哈希算法（SHA2系列）。它适用于加密安全目的。除非具有特定的代码大小限制，否则建议使用MicroPython内核和任何板提供此功能。

* SHA1 - 上一代算法。不建议用于新用途，但SHA1是许多Internet标准和现有应用程序的一部分，因此针对网络连接和互操作性的板将尝试提供此功能。

* MD5 - 遗留算法，不被认为是加密安全的。只有选定的电路板才能实现与传统应用的互操作性。

构建对象
------------

.. class:: uhashlib.sha256([data])

    创建一个SHA256哈希对象，并可选择 ``data`` 输入其中。
    Create an SHA256 hasher object and optionally feed ``data`` into it.

.. class:: uhashlib.sha1([data])

    创建一个SHA1哈希对象，并可选择 ``data`` 将其输入其中。

.. class:: uhashlib.md5([data])

    创建MD5哈希对象并可选择 ``data`` 将其输入其中。

方法
-------

.. method:: hash.update(data)

   将更多的二进制数据馈入散列

.. method:: hash.digest()

  返回通过哈希传递的所有数据的散列，作为字节对象。调用此方法后，无法再将更多的数据送入散列。

.. method:: hash.hexdigest()

  此方法未实现。使用 ``ubinascii.hexlify(hash.digest())`` 来达到类似的效果。


