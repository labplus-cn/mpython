.. _array_lib:
:mod:`array` -- 数值数组
======================================

.. module:: array
   :synopsis: 高效的数值数组

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `array <https://docs.python.org/3.5/library/array.html#module-array>`_

支持的格式的代码： ``b``, ``B``, ``h``, ``H``, ``i``, ``I``, ``l``,
``L``, ``q``, ``Q``, ``f``, ``d`` (后者2取决于浮点支持).

Classes
-------

.. class:: array.array(typecode, [iterable])

   使用给定类型的元素创建数组。数组的初始内容由 `iterable` 给出。如果未提供，则创建空数组。

    .. method:: append(val)

       将新元素val附加到数组的末尾，使其增长.

    .. method:: extend(iterable)

       将迭代中包含的新元素追加到数组的末尾，增长它.
