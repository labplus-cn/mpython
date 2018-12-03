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



HTTP Server
----------------

以下示例，掌控板作为HTTP服务端，使用浏览器可以访问板载光线传感器::

    import socket
    import network,time
    from mpython import *

    mywifi=wifi()     #实例化wifi类

    mywifi.connectWiFi("ssid","password")                  # WiFi连接，设置ssid 和password

    CONTENT = b"""\
    HTTP/1.0 200 OK

    <meta charset="utf-8">
    欢迎使用mPython！你的光线传感器值是:%d
    """

    def main():
        s = socket.socket()
        ai = socket.getaddrinfo(mywifi.sta.ifconfig()[0], 80)
        print("Bind address info:", ai)
        addr = ai[0][-1]
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(5)
        print("Listening, connect your browser to http://%s:80/" %addr[0])
        oled.DispChar('Connect your browser',0,0,)                       #oled显示掌控板ip地址
        oled.DispChar('http://%s' %addr[0],0,16)
        oled.show()
        while True:
            res = s.accept()
            client_s = res[0]
            client_addr = res[1]
            print("Client address:", client_addr)
            print("Client socket:", client_s)
            req = client_s.recv(4096)
            print("Request:")
            print(req)
            client_s.send(CONTENT % light.read())
            client_s.close()




在REPL中运行main::

    >>> main()

.. image:: /images/tutorials/http_1.png


手机或笔记本电脑连接相同wifi，使其在同个局域网内。按打印提示或oled屏幕显示ip，使用浏览器访问掌控板主机IP地址。

.. image:: /images/tutorials/http_2.png


