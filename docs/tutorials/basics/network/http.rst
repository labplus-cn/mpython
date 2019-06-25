HTTP
=======

HTTP是基于客户端/服务端（C/S）的架构模型，通过一个可靠的链接来交换信息，是一个无状态的请求/响应协议。

一个HTTP"客户端"是一个应用程序（Web浏览器或其他任何客户端），通过连接到服务器达到向服务器发送一个或多个HTTP的请求的目的。

HTTP GET request
----------------

以下示例显示了如何下载网页。HTTP使用端口80，您首先需要发送“GET”请求才能下载任何内容。作为请求的一部分，您需要指定要检索的页面。

让我们定义一个可以下载和打印URL的函数::

    import socket

    def http_get(url):
        _, _, host, path = url.split('/', 3)
        addr = socket.getaddrinfo(host, 80)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
        while True:
            data = s.recv(100)
            if data:
                print(str(data, 'utf8'), end='')
            else:
                break
        s.close()

.. Hint::

    在使用socket模块时，请先连接wifi，并且确保可以访问互联网。有关如何wifi连接，请查看上章节 :ref:`配置wifi<network_base>` 。

然后您可以尝试：

    >>> http_get('http://micropython.org/ks/test.html')


此时接收到html网页并打印到终端。


urequest 模块
~~~~~~~~~~~~~

上面是使用socket来实现http的get请求。我们可以使用 :mod:`urequests` 模块,里面已封装HTTP协议一些常用的请求方式,使用更为简便。

::

    import urequests
    from mpython import *

    my_wifi = wifi()
    my_wifi.connectWiFi('ssid','psw')

    # http get方法
    r = urequests.get('http://micropython.org/ks/test.html')
    # 响应的内容
    r.contens

有关更多的 :mod:`urequests` 模块使用,请查阅该模块说明。

HTTP Server
----------------

.. literalinclude:: /../examples/06.网络/http_server_simplistic.py
    :caption: 以下示例，掌控板作为HTTP服务端，使用浏览器可以访问板载光线传感器:
    :linenos:


在REPL中运行main::

    >>> main()

.. image:: /images/tutorials/http_1.png


手机或笔记本电脑连接相同wifi，使其在同个局域网内。按打印提示或oled屏幕显示ip，使用浏览器访问掌控板主机IP地址。

.. image:: /images/tutorials/http_2.png



