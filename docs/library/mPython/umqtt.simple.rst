
.. _umqtt.simple:
:mod:`umqtt.simple`

umqtt.simple 模块
=========================================

MQTT是一种基于发布 - 订阅的“轻量级”消息传递协议，用于在TCP / IP协议之上使用。
提供订阅/发布模式，更为简约、轻量，易于使用，针对受限环境（带宽低、网络延迟高、网络通信不稳定），可以简单概括为物联网打造。

.. Hint:: 

    该模块来源于 ``MicroPython-lib`` : https://github.com/micropython/micropython-lib/tree/master/umqtt.simple

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

.. method:: MQTTClient.set_callback(f)

    - ``f`` - f(topic, msg) 为回调函数,第1参数为 ``topic`` 接收到的主题,第2参数为 ``msg`` 为该主题消息



为收到的订阅消息设置回调

.. method:: MQTTClient.set_last_will(topic, msg, retain=False, qos=0)

设置MQTT“last will”消息。应该在 connect()之前调用。

.. method:: MQTTClient.connect( clean_session=True )

连接到服务器。如果此连接使用存储在服务器上的持久会话，则返回True（如果使用clean_session = True参数，则返回False（默认值））。

.. method:: MQTTClient.disconnect()

断开与服务器的连接，释放资源。

.. method:: MQTTClient.ping()

Ping服务器（响应由wait_msg（）自动处理）

.. method:: MQTTClient.publish(topic, msg, retain=False, qos=0)

发布消息

.. method:: MQTTClient.subscribe(topic, qos=0)

订阅主题

.. method:: MQTTClient.wait_msg()

等待服务器消息。订阅消息将通过set_callback（）传递给回调集，任何其他消息都将在内部处理。

.. method:: MQTTClient.check_msg()

检查服务器是否有待处理的消息。如果是，则以与wait_msg（）相同的方式处理，如果不是，则立即返回。


.. Attention:: 

    * wait_msg()并且check_msg()是“主循环迭代”方法，阻塞和非阻塞版本。wait_msg()如果您没有任何其他前台任务要执行（即您的应用只响应订阅的MQTT消息），check_msg() 如果您也处理其他前台任务，则应定期在循环中调用它们 。
    * 请注意，如果您只发布消息，则不需要调用wait_msg()/ check_msg()，也不要订阅消息。
    * 发布和订阅都支持QoS 0和1。不支持QoS2以保持较小的代码大小。除ClientID外，目前只支持“clean session”参数进行连接。

