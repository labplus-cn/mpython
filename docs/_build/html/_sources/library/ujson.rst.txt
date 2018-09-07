:mod:`ujson` -- JSON 编码和解码
==========================================

.. module:: ujson
   :synopsis: JSON 编码和解码

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `json <https://docs.python.org/3.5/library/json.html#module-json>`_

This modules allows to convert between Python objects and the JSON
data format.

Functions
---------

.. function:: dumps(obj)

   Return ``obj`` represented as a JSON string.

.. function:: loads(str)

   Parse the JSON ``str`` and return an object.  Raises ValueError if the
   string is not correctly formed.
