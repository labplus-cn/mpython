:mod:`uerrno` -- 系统错误代码
===================================

.. module:: uerrno
   :synopsis: 系统错误代码

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `errno <https://docs.python.org/3.5/library/errno.html#module-errno>`_

此模块提供访问符号错误代码以进行 :ref:`OSError <OSError>`  异常。特定的代码清单依赖于 :term:`MicroPython port`.


常量
---------

.. data:: EEXIST, EAGAIN, etc.

    错误代码，基于ANSI C/POSIX标准。所有错误代码开头都有“E”。错误通常可以访问为 ``exc.args[0]`` ，其中 ``exc`` 是 ``OSError`` 的一个实例

    示例::

        try:
            uos.mkdir("my_dir")
        except OSError as exc:
            if exc.args[0] == uerrno.EEXIST:
                print("Directory already exists")

.. data:: errorcode

    字典将数字错误代码映射到带有符号错误代码的字符串（参见上文）::

        >>> print(uerrno.errorcode[uerrno.EEXIST])
        EEXIST
