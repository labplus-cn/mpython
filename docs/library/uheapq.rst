:mod:`uheapq` -- 堆队列算法
=====================================

.. module:: uheapq
   :synopsis: 堆队列算法

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `heapq <https://docs.python.org/3.5/library/heapq.html#module-heapq>`_

This module implements the heap queue algorithm.

A heap queue is simply a list that has its elements stored in a certain way.

Functions
---------

.. function:: heappush(heap, item)

   Push the ``item`` onto the ``heap``.

.. function:: heappop(heap)

   Pop the first item from the ``heap``, and return it.  Raises IndexError if
   heap is empty.

.. function:: heapify(x)

   Convert the list ``x`` into a heap.  This is an in-place operation.
