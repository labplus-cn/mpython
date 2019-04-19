.. _radio:
radio 模块
==========

radio 模块提供无线广播功能,支持14 Channel,在相同的Channel内能接收到成员发出的广播消息。

函数
----------


.. py:method:: radio.on()

开启无线功能

.. py:method:: radio.off()

关闭无线功能


.. py:method:: radio.config(channel)


配置无线参数

- ``channel`` (int): 无线通道,范围1~14



.. py:method:: radio.receive()

接收无线广播消息,消息以字符串形式返回。最大可接收250字节数据。如果没有接收到消息,则返回 ``None`` 。当 ``receive`` 内参数为 ``True`` ,即 ``receive(True)`` ,返回(msg,mac)的二元组。默认缺省 ``receive(False)`` ,即只返回msg。


.. py:method:: radio.receive_bytes()

接收无线广播消息,消息以字节形式返回。其他同 ``radio.receive()`` 相同。

.. py:method:: radio.send()

发送无线广播消息,发送数据类型为字符串

.. py:method:: radio.send_bytes()

发送无线广播消息,发送数据类型为字节