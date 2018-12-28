
.. _umqtt.simple:
:mod:`umqtt.simple`

umqtt.simple 模块
=========================================

MQTT是一种基于发布 - 订阅的“轻量级”消息传递协议，用于在TCP / IP协议之上使用。
提供订阅/发布模式，更为简约、轻量，易于使用，针对受限环境（带宽低、网络延迟高、网络通信不稳定），可以简单概括为物联网打造。


构建对象
-------------

.. class:: MQTTClient(client_id, server, port=0, user=None, password=None, keepalive=0,ssl=False, ssl_params={})

    - ``client_id``
    - ``server``
    - ``port``
    - ``user``
    - ``password``
    - ``keepalive``
    - ``ssl``
    - ``ssl_params``

方法
--------

.. method:: set_callback()