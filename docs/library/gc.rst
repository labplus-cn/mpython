:mod:`gc` --  回收内存碎片
==========================================

.. module:: gc
   :synopsis:  回收内存碎片

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档:`array <https://docs.python.org/3.5/library/gc.html#module-gc>`_.

Functions
---------

.. function:: enable()

   启用自动回收内存碎片。

.. function:: disable()

  禁用自动回收。堆内存仍然可以分配，但可以通过 :meth:`gc.collect` 函数进行手动回收内存碎片。


.. function:: collect()

   回收内存碎片。

.. function:: mem_alloc()

  返回分配的堆RAM的字节数.

   .. admonition:: 与CPython的区别
      :class: attention
      

      此功能是MicroPython扩展.

.. function:: mem_free()

   返回可用堆RAM的字节数，如果此数量未知，则返回-1.

   .. admonition:: 与CPython的区别
      :class: attention

       此功能是MicroPython扩展.

.. function:: isenabled()

  判断是否启动自动内存碎片收集。

.. function:: threshold([amount])

   设置或查询其他GC分配阈值。通常，只有在无法满足新分配时，即在内存不足（OOM）条件下才会触发集合。
   如果调用此函数，除了OOM之外，每次分配了大量字节后都会触发一个集合（总共，因为上一次分配了这么多的字节）。
   amount通常被指定为小于完整堆大小，意图在堆耗尽之前触发集合，并希望早期集合可以防止过多的内存碎片。
   这是一种启发式度量，其效果因应用程序而异，以及量参数的最佳值。

   不带参数调用函数将返回阈值的当前值。值-1表示禁用的分配阈值。

   .. admonition:: 与CPython的区别
      :class: attention

      函数是MicroPython扩展。CPython具有类似的功能 - ``set_threshold()`` 但由于不同的GC实现，它的签名和语义是不同的。
