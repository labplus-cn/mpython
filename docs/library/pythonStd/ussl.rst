:mod:`ussl` -- SSL/TLS module
=============================

.. module:: ussl
   :synopsis: TLS/SSL wrapper for socket objects

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `ssl <https://docs.python.org/3.5/library/ssl.html#module-ssl>`_

此模块提供对客户端和服务器端网络套接字的传输层安全性（以前称为“安全套接字层”）加密和对等身份验证工具的访问。

Functions
---------

.. function:: ssl.wrap_socket(sock, server_side=False, keyfile=None, certfile=None, cert_reqs=CERT_NONE, ca_certs=None)


采用流sock（通常是SOCK_STREAM类型的usocket.socket实例），并返回ssl.SSLSocket的实例，该实例将基础流包装在SSL上下文中。
返回的对象具有通常的流接口方法，如 read()，write()等。
在MicroPython中，返回的对象不公开套接字接口和方法，如recv()，send()。
特别是，应该从accept()非SSL侦听服务器套接字上返回的普通套接字创建服务器端SSL 套接字。




.. warning::

    模块的某些实现不验证服务器证书，这使得建立的SSL连接容易发生中间人攻击。

异常
----------

.. data:: ssl.SSLError

   此异常不存在。而是使用它的基类OSError。

常量
---------

.. data:: ssl.CERT_NONE
          ssl.CERT_OPTIONAL
          ssl.CERT_REQUIRED

    cert_reqs参数支持的值。
