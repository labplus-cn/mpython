:mod:`uselect` -- wait for events on a set of streams
========================================================================

.. module:: uselect
   :synopsis: wait for events on a set of streams

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `select <https://docs.python.org/3.5/library/select.html#module-select>`_

该模块提供了有效等待多个 :term:`stream` （选择可用于操作的流）上的事件的功能。

函数
---------

.. function:: poll()

创建一个Poll类的实例。

.. function:: select(rlist, wlist, xlist[, timeout])

等待一组对象上的活动。

该功能由一些MicroPython端口提供，以实现兼容性并且效率不高。 :class:`Poll`  推荐使用。


.. _class: Poll

类 Poll
--------------

方法
~~~~~~~

.. method:: poll.register(obj[, eventmask])

   注册obj进行轮询。事件掩码是逻辑或：

   * ``select.POLLIN``  - 可阅读的数据
   * ``select.POLLOUT`` - 可以写更多的数据
   * ``select.POLLERR`` - 发生了错误
   * ``select.POLLHUP`` - 检测到流/连接终止

   *eventmask* 默认为 ``select.POLLIN | select.POLLOUT``.

.. method:: poll.unregister(obj)

   从投票中注销 ``obj`` 。

.. method:: poll.modify(obj, eventmask)

   修改eventmask的 ``OBJ`` 。

.. method:: poll.poll([timeout])

   等待至少一个注册对象准备就绪。返回（``obj`` , ``event`` , …）元组的列表， ``event`` 元素指定使用流发生的事件，
   并且是 ``select.POLL*``  上述常量的组合。在tuple中可能还有其他元素，具体取决于平台和版本，因此不要认为它的大小是2.
   如果超时，返回一个空列表。

   超时是毫秒。


   .. admonition:: Difference to CPython
      :class: attention

      Tuples returned may contain more than 2 elements as described above.

.. method:: poll.ipoll(timeout=-1, flags=0)

   Like :meth:`poll.poll`, but instead returns an iterator which yields
   `callee-owned tuples`. This function provides efficient, allocation-free
   way to poll on streams.

   If *flags* is 1, one-shot behavior for events is employed: streams for
   which events happened, event mask will be automatically reset (equivalent
   to ``poll.modify(obj, 0)``), so new events for such a stream won't be
   processed until new mask is set with `poll.modify()`. This behavior is
   useful for asynchronous I/O schedulers.

   .. admonition:: Difference to CPython
      :class: attention

      This function is a MicroPython extension.
