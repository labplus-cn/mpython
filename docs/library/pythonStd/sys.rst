:mod:`sys` -- 系统特定功能
=======================================

.. module:: sys
   :synopsis: 系统特定功能


sys模块中提供了与MicroPython运行环境有关的函数和变量。

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `sys <https://docs.python.org/3.5/library/sys.html#module-sys>`_

Functions
---------

.. function:: exit(retval=0)

   使用给定的退出代码终止当前程序。在此基础上，此功能提升为 ``SystemExit`` 。如果给出一个参数，则将其值作为参数给出 ``SystemExit``  。

.. function:: print_exception(exc, file=sys.stdout)


    通过回溯到类文件对象文件（或 ``sys.stdout`` 默认情况下）来打印异常。

   .. admonition:: 与CPython的区别
      :class: attention

        这是 ``traceback``  CPython模块中出现的函数的简化版本 。与 ``traceback.print_exception()`` 此不同，此函数仅使用异常值而不是异常类型，异常值和回溯对象; file参数应该是位置的; 不支持其他参数。
        ``traceback``  可以找到CPython兼容 模块 ``micropython-lib`` 。

常量
---------

.. data:: argv

    当前程序启动的可变参数列表。

.. data:: byteorder

    系统的字节顺序（ ``little`` 或 ``big`` ）。

.. data:: implementation

    包含有关当前Python实现的信息的对象。对于MicroPython，它具有以下属性：

    * *name* - 字符串 "micropython"
    * *version* - 元组 (major, minor, micro), e.g. (1, 7, 0)

    这个方法推荐用来识别不同平台的MicroPython。


    示例::

        >>> print(sys.implementation)
        (name='micropython', version=(1, 9, 1))

.. data:: maxsize

    本机整数类型可以在当前平台上保存的最大值，或MicroPython整数类型可表示的最大值，如果它小于平台最大值
    （对于没有长int支持的MicroPython端口的情况）。

    此属性对于检测平台的“位数”（32位与64位等）非常有用。建议不要直接将此属性与某个值进行比较，而是计算其中的位数::

        bits = 0
        v = sys.maxsize
        while v:
            bits += 1
            v >>= 1
        if bits > 32:
            # 64-bit (or more) platform
            ...
        else:
            # 32-bit (or less) platform
            # Note that on 32-bit platform, value of bits may be less than 32
            # (e.g. 31) due to peculiarities described above, so use "> 16",
            # "> 32", "> 64" style of comparisons.

.. data:: modules

    已载入模块字典。在某些移植版中，它可能不包含在内建模块中。

.. data:: path

    用于搜索导入模块的可变目录列表。

.. data:: platform

   获取MicroPython运行的平台。

.. data:: stderr

  标准错误 ``stream``

.. data:: stdin

   标准输入 ``stream``

.. data:: stdout

   标准输出 ``stream``

.. data:: version

    返回 MicroPython 语言版本，字符串

.. data:: version_info

   返回 MicroPython 语言版本，整形元组
