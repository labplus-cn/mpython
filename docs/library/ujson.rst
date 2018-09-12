:mod:`ujson` -- JSON 编码和解码
==========================================

.. module:: ujson
   :synopsis: JSON 编码和解码

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `json <https://docs.python.org/3.5/library/json.html#module-json>`_

该模块提供json数据格式的转换。

Functions
---------

.. function:: dumps(obj)

  将dict类型的数据转换成str，因为如果直接将dict类型的数据写入json文件中会发生报错，因此在将数据写入时需要用到该函数。

  - ``obj`` 要转换的对象


.. function:: loads(str)

   解析 JSON 字符串并返回对象。如果字符串格式错误将引发 ValueError 异常。 
