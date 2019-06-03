.. _tutorials_radio:

无线广播
===============

掌控板提供2.4G的无线射频通讯,共 13 Channel。可实现一定区域内的简易组网通讯。在相同通道下,成员可接收广播消息。就类似,对讲机一样。在相同频道下,实现通话。

.. figure:: /images/tutorials/radio/radio.png
    :align: center
    :width: 200

    对讲机

radio
--------

.. literalinclude:: /../examples/radio/radio.py
    :caption: 你可以用两块掌控板上传该程序,在REPL下,发送和接收广播消息
    :linenos:

|

.. raw:: html

    <iframe width="700" height="400" src="https://showmore.com/zh/embed/j9xqz8v"  frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>

|

首先我们需要 ``import radio`` ,导入无线模块。然后 ``radio.on()`` ,开启无线功能。配置无线通道 ``radio.config(channel)`` ,channel参数可设置1~13个通道。
使用 ``radio.send()`` 发送广播消息,消息类型为字符串。接收端,在相同channel,使用 ``radio.receive()`` 来接收广播数据。 ``receive(True)`` 返回数据类型为(msg,mac)。
mac为网络设备的MAC地址,地址均唯一。如,想做单播应用,可过滤其他MAC设备发送的消息。默认下 ``receive()`` ,返回的数据类型为msg,是不带MAC地址的。


电报机
-------

基于上面的radio学习,我们可以用掌控板制作个有趣的电报机！两个掌控板之间通过无线电和摩斯密码传播,是不是有谍战片的既视感咧！赶紧尝试下吧！

.. figure:: /images/tutorials/radio/telegraph.jpg
    :align: center
    :width: 400

    电报机


.. literalinclude:: /../examples/radio/telegraph.py
    :caption: 电报机示例
    :linenos:

|
.. raw:: html

    <iframe width="700" height="400" src="https://showmore.com/zh/embed/ra3i9uw"  frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>

|

上述电报机示例,ab按键选择无线通道,触摸T,发送电报。当接收到电报,掌控板的RGB会有指示。