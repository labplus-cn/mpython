:mod:`ucollections` -- 容器数据类型
=====================================================

.. module:: ucollections
   :synopsis: 容器数据类型

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `collections <https://docs.python.org/3.5/library/collections.html#module-collections>`_

此模块实现高级集合和容器类型以保存/累积各种对象。

类
-------

.. function:: deque(iterable, maxlen[, flags])

    Deques（双端队列）是一个类似列表的容器，支持O（1）追加并从双端队列的任一侧弹出。使用以下参数创建新的deques：

    * iterable必须是空元组，并且新的deque创建为空。
    * 必须指定maxlen并将双端队列限制为此最大长度。一旦双端队列已满，添加的任何新项目将丢弃对方的项目。
    * 添加项目时，可选标志可以为1以检查溢出。

    除了支持 ``bool`` 和 ``len`` deque对象还有以下方法：

     .. method:: deque.append(x)

    在deque的右边加上x。如果启用溢出检查，并且没有剩余的空间，则会引发索引错误。

     .. method:: deque.popleft()

     从deque的左侧移除并返回一个项目。如果没有项出现，就会引起索引错误。


.. function:: namedtuple(name, fields)

    这是工厂功能，用于创建一个具有特定名称和一组字段的新的namedtuple类型。
    一个namedtuple是元组的子类，它允许不仅通过数字索引来访问它的字段，而且使用符号字段名称的属性访问语法。
    字段是指定字段名称的字符串序列。为了与CPython兼容，它也可以是一个名为空格分隔字段的字符串（但效率较低）。

    使用示例::

        from ucollections import namedtuple

        MyTuple = namedtuple("MyTuple", ("id", "name"))
        t1 = MyTuple(1, "foo")
        t2 = MyTuple(2, "bar")  
        print(t1.name)
        assert t2.name == t2[1]

.. function:: OrderedDict(...)

    ``dict`` 类型子类，它能记住和保留添加的keys的顺序。当遍历有序字典时，keys/items按照添加的顺序返回::

        from ucollections import OrderedDict

        # To make benefit of ordered keys, OrderedDict should be initialized
        # from sequence of (key, value) pairs.
        d = OrderedDict([("z", 1), ("a", 2)])
        # More items can be added as usual
        d["w"] = 5
        d["b"] = 3
        for k, v in d.items():
            print(k, v)

    Output::

        z 1
        a 2
        w 5
        b 3
