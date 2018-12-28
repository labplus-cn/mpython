
.. _urequests:
:mod:`urequests`

urequests 模块
================

之前我们用了 socket 库，这个作为入门的工具还是不错的，对了解一些爬虫的基本理念，掌握爬虫爬取的流程有所帮助。
入门之后，我们就需要学习一些更加高级的内容和工具来方便我们的爬取。
那么这一节来简单介绍一下 urequests 库的基本用法。

Response类
---------

.. class:: Response(s)

该Response类的对象，包含服务器对HTTP请求的响应。

    - ``s``-ussl对象

方法
~~~~~~~

.. method:: close()

关闭socket。

.. decorator:: content

返回响应的内容，以字节为单位。

.. decorator:: text

以文本方式返回响应的内容，编码为unicode。

.. method:: json()

返回响应的json编码内容并转为dict类型。

方法
---------

.. method:: request(method, url, data=None, json=None, headers={},params=None)

向服务器发送HTTP请求。

    - ``method`` - 要使用的HTTP方法
    - ``url`` - 要发送的URL
    - ``data`` - 要附加到请求的正文。如果提供字典或元组列表，则将进行表单编码。
    - ``json`` - json用于附加到请求的主体。
    - ``headers`` - 要发送的标头字典。
    - ``params`` - 附加到URL的URL参数。如果提供字典或元组列表，则将进行表单编码。

.. method:: head(url, **kw)

发送HEAD请求,返回Response对象。

    - ``url`` - Request对象的URL
    - ``**kw`` - request方法的参数。

.. method:: get(url, **kw)

发送GET请求,返回Response对象。

    - ``url`` - Request对象的URL
    - ``**kw`` - request方法的参数。

.. method:: post(url, **kw)

发送POST请求,返回Response对象。

    - ``url`` - Request对象的URL
    - ``**kw`` - request方法的参数。
    

.. method:: put(url, **kw)

发送PUT请求,返回Response对象。

    - ``url`` - Request对象的URL
    - ``**kw`` - request方法的参数。
    
.. method:: patch(url, **kw)

送PATCH请求,返回Response对象。

    - ``url`` - Request对象的URL
    - ``**kw`` - request方法的参数。


    
.. method:: delete(url, **kw)

发送DELETE请求。,返回Response对象。

    - ``url`` - Request对象的URL
    - ``**kw`` - request方法的参数。

