:mod:`uerrno` -- 系统错误代码
===================================

.. module:: uerrno
   :synopsis: 系统错误代码

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `errno <https://docs.python.org/3.5/library/errno.html#module-errno>`_

This module provides access to symbolic error codes forr  :ref:`OSError <OSError>`  exception.
A particular inventory of codes depends on  :term:`MicroPython port`.

Constants
---------

.. data:: EEXIST, EAGAIN, etc.

    Error codes, based on ANSI C/POSIX standard. All error codes start with
    "E". As mentioned above, inventory of the codes depends on
    `MicroPython port`. Errors are usually accessible as ``exc.args[0]``
    where `exc` is an instance of `OSError`. Usage example::

        try:
            uos.mkdir("my_dir")
        except OSError as exc:
            if exc.args[0] == uerrno.EEXIST:
                print("Directory already exists")

.. data:: errorcode

    Dictionary mapping numeric error codes to strings with symbolic error
    code (see above)::

        >>> print(uerrno.errorcode[uerrno.EEXIST])
        EEXIST
