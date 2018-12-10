:mod:`select` -- 等待流事件
========================================================================

.. module:: select
   :synopsis: wait for events on a set of streams

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `select <https://docs.python.org/3.5/library/select.html#module-select>`_

该模块提供了有效等待多个 :term:`stream` （选择可用于操作的流）上的事件的功能。

函数
---------

.. function:: poll()

创建轮询实例。

.. function:: select(rlist, wlist, xlist[, timeout])

监控对象何时可读或可写，一旦监控的对象状态改变，返回结果（阻塞线程）。
这个函数是为了兼容，效率不高，推荐用 poll 函数。

- ``rlist``：等待读就绪的文件描述符数组
- ``wlist``：等待写就绪的文件描述符数组
- ``xlist``：等待异常的数组
- ``timeout``：等待时间（单位：秒）


.. _class: Poll

类 Poll
--------------

方法
~~~~~~~

.. method:: poll.register(obj, flag)

   注册一个用以监控的对象，并设置被监控对象的监控标志位flag。

   - ``obj`` :被监控的对象
   - ``flag`` :被监控的标志

    - ``select.POLLIN``  - 读取可用数据
    - ``select.POLLOUT`` - 写入更多数据
    - ``select.POLLERR`` - 发生错误
    - ``select.POLLHUP`` - 流结束/连接终止检测

   ``flag`` 默认为 ``select.POLLIN | select.POLLOUT``.

.. method:: poll.unregister(obj)

   解除监控的对象``obj`` 的注册。

.. method:: poll.modify(obj, flag)

   修改已注册的对象 ``obj`` 监控标志 ``flag`` 。

.. method:: poll.poll([timeout])

   等待至少一个注册对象准备就绪。返回（``obj`` , ``event`` , …）元组的列表， ``event`` 元素指定使用流发生的事件，
   并且是 ``select.POLL*``  上述常量的组合。在tuple中可能还有其他元素，具体取决于平台和版本，因此不要认为它的大小是2.
   如果超时，返回一个空列表。

   超时是毫秒。


   .. admonition:: Difference to CPython
      :class: attention

      Tuples returned may contain more than 2 elements as described above.

.. method:: poll.ipoll([timeout])

   与 :meth:`poll.poll` 类似，但是返回一个产生被调用函数所有元组的迭代器。该函数提供高效的、无位置的在流中进行轮询的方法。


   .. admonition:: 与CPython区别
      :class: attention

      该函数是MicroPython的扩展。
