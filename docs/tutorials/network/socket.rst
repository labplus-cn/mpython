TCP套接字
================

大多数互联网的构建都是使用TCP套接字。这些套接字在连接的网络设备之间提供可靠的字节流。
本教程的这一部分将介绍如何在几种不同的情况下使用TCP套接字。

HTTP GET request
----------------
HTTP是基于客户端/服务端（C/S）的架构模型，通过一个可靠的链接来交换信息，是一个无状态的请求/响应协议。

一个HTTP"客户端"是一个应用程序（Web浏览器或其他任何客户端），通过连接到服务器达到向服务器发送一个或多个HTTP的请求的目的。

下下示例显示了如何下载网页。HTTP使用端口80，您首先需要发送“GET”请求才能下载任何内容。作为请求的一部分，您需要指定要检索的页面。

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

然后你可以尝试：

    >>> http_get('http://micropython.org/ks/test.html')


此时接收到html网页并打印到终端。



HTTP Server
----------------