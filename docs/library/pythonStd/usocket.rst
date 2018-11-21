*******************************
:mod:`usocket` -- socket 模块
*******************************

.. module:: usocket
   :synopsis: socket 模块

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `socket <https://docs.python.org/3.5/library/socket.html#module-socket>`_

该模块提供BSD socket接口的访问。

.. admonition:: 与CPython区别
   :class: attention

    为提高效率与一致性，MicroPython中的套接字对象直接实现流（类文件）接口。在CPython中，
    需使用 ``makefile()`` 方法来将socket转换为类文件对象。该方法仍由MicroPython（但是是无操作）支持，
    所以在CPython的兼容性问题上，请一定使用该方法。

Socket地址格式
------------------------

下面函数使用 (ipv4_address, port) 网络地址, ipv4_address 是由点和数字组成的字符串，如 ``"8.8.8.8"`` ，
端口是 1-65535 的数字。注意不能使用域名做为 ipv4_address，域名需要先用 ``socket.getaddrinfo()`` 进行解析。

``usocket`` 模块的本机套接字地址格式是一个由 ``getaddrinfo`` 函数返回的不透明数据类型，
须用其来解析文本地址（包括数字型地址）::

    sockaddr = usocket.getaddrinfo('www.micropython.org', 80)[0][-1]
    # You must use getaddrinfo() even for numeric addresses 您必须使用getaddrinfo()，即使是用于数字型地址
    sockaddr = usocket.getaddrinfo('127.0.0.1', 80)[0][-1]
    # Now you can use that address 现在您可以使用这一地址了
    sock.connect(addr)

使用 ``getaddrinfo`` 是处理地址最有效（在内存和处理能力方面皆是如此）且最便捷的方式。


函数
---------

.. function:: socket(af=AF_INET, type=SOCK_STREAM, proto=IPPROTO_TCP)

  - ``af`` ：地址

    - ``socket.AF_INET``:=2 — TCP/IP – IPv4
    - ``socket.AF_INET6`` :=10 — TCP/IP – IPv6

  - ``type`` ：socket类型

    - ``socket.SOCK_STREAM``:=1 — TCP流
    - ``socket.SOCK_DGRAM``:=2 — UDP数据报
    - ``socket.SOCK_RAW`` :=3 — 原始套接字
    - ``socket.SO_REUSEADDR`` : =4 — socket可重用

  - ``proto`` ：协议号

    - ``socket.IPPROTO_TCP`` =16
    - ``socket.IPPROTO_UDP`` =17 


一般不指定proto参数，因为有些MicroPython固件提供默认参数::

  >>> s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  >>> print(s)
  <socket>

.. function:: getaddrinfo(host, port)

将主机域名（host）和端口（port）转换为用于创建套接字的5元组序列。元组列表的结构如下::

  (family, type, proto, canonname, sockaddr)

下面显示了怎样连接到一个网址::

  s = usocket.socket()
  s.connect(usocket.getaddrinfo('www.micropython.org', 80)[0][-1])

.. admonition:: 与CPython区别
  :class: attention

    该函数发生错误时，会引发一个 ``socket.gaierror`` 异常（ ``OSError`` 子类）。 
    MicroPython并不具有 ``socket.gaierror`` ，会直接引发OSError。 
    注意： ``getaddrinfo()`` 的错误数量组成一个单独的名称空间，
    可能与 ``uerrno`` 系统错误代码模块中的错误数量不匹配。
    为区分 ``getaddrinfo()`` 错误，该错误使用负数标记，标准系统错误为正数（错误数可通过使用异常对象的 e.args[0] 特性访问）。
    暂时使用负数，未来可能改变。



socket类
============

方法
-------

.. method:: socket.close()

关闭socket。一旦关闭后，socket所有的功能都将失效。远端将接收不到任何数据 (清理队列数据后)。
内存碎片回收时socket会自动关闭，但还是推荐在必要时用 close() 去关闭

.. method:: socket.bind(address)

以列表或元组的方式绑定地址和端口号。

  - ``address`` ：一个包含地址和端口号的列表或元组。

示例::

  addr = ("127.0.0.1",10000)
  s.bind(addr)




.. method:: socket.listen([backlog])

监听socket，使服务器能够接收连接。如果指定了 ``backlog`` ，它不能小于0 (如果小于0将自动设置为0)；
超出后系统将拒绝新的连接。如果没有指定，将使用默认值。

  -  ``backlog`` ：接受套接字的最大个数，至少为0，如果没有指定，则默认一个合理值。

   

.. method:: socket.accept()


接收连接请求。socket需要指定地址并监听连接。返回值是 (conn, address)，
其中conn是用来接收和发送数据的套接字，address是绑定到另一端的套接字。
  
  - ``conn``：新的套接字对象，可以用来收发消息
  - ``address``：连接到服务器的客户端地址

.. admonition::

  只能在绑定地址端口号和监听后调用，返回conn和address。



.. method:: socket.connect(address)

连接到指定地址的服务器。

  - ``address``：服务器地址和端口号的元组或列表

示例::

  host = "192.168.3.147"
  port = 100
  s.connect((host, port))

.. method:: socket.send(bytes)

发送数据，并返回发送的字节数。

  - ``bytes``：bytes类型数据

.. method:: socket.sendall(bytes)

与send(）函数类似，区别是sendall()函数通过数据块连续发送数据。

  - ``bytes``：bytes类型数据



.. method:: socket.recv(bufsize)

接收数据，返回接收到的数据对象。

  - ``bufsize``：指定一次接收的最大数据量

示例::

  data = conn.recv(1024)



.. method:: socket.sendto(bytes, address)

发送数据，目标由address决定，用于UDP通信，返回发送的数据大小。

  - ``bytes``：bytes类型数据
  - ``address``：目标地址和端口号的元组


.. method:: socket.recvfrom(bufsize)

接收数据，用于UDP通信，并返回接收到的数据对象和对象的地址。

  - ``bufsize``：指定一次接收的最大数据量

.. method:: socket.setsockopt(level, optname, value)

根据选项值设置socket。

  - ``level``：套接字选项级别
  - ``optname``：socket 选项
  - ``value``：可以是一个整数，也可以是一个表示缓冲区的bytes类对象。

示例::

  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

.. method:: socket.settimeout(value)

设置超时时间，单位：秒。 

示例::

  s.settimeout(2)

.. method:: socket.setblocking(flag)

设置socket的阻塞或非阻塞模式：若标记为false，则将该socket设置为非阻塞模式，而非阻塞模式。

该方法为某些settimeout()调用的简写:

   * ``sock.setblocking(True)`` is equivalent to ``sock.settimeout(None)``
   * ``sock.setblocking(False)`` is equivalent to ``sock.settimeout(0)``

.. method:: socket.makefile(mode='rb', buffering=0)

返回一个与socket相关联的文件对象。具体的返回类型取决于给定makefile()的参数。该支持仅限于二进制模式（‘rb’和‘wb’）.

CPython的参数为：不支持 encoding 、 errors 、 newline 。

Socket须为阻塞模式；允许超时存在，但若出现超时，文件对象的内部缓冲区可能会以不一致状态结束。

.. admonition:: 与CPython区别
  :class: attention

  * 由于MicroPython不支持缓冲流，则将忽略缓冲参数的值，且将按照该值为0（未缓冲）时处理。
  * 关闭所有由makefile()返回的文件对象，同样将关闭原始socket。

.. method:: socket.read([size])

从socket中读取size字节。返回一个字节对象。若未给定 ``size`` ，则按照类似 :meth:`socket.readall()` 的模式运行，见下。


.. method:: socket.readinto(buf[, nbytes])


将字节读取入缓冲区。若指定 nbytes ，则最多读取该数量的字节。否则，最多读取 len(buf) 数量的字节。
正如 ``read()`` ，该方法遵循“no short reads”方法。

返回值：读取并存入缓冲区的字节数量


.. method:: socket.readline()

接收一行数据，遇换行符结束，并返回接收数据的对象 。


.. method:: socket.write(buf)


向字节缓冲区写入socket，并返回写入数据的大小。



常数
------

.. data:: AF_INET
          AF_INET6

   地址簇

.. data:: SOCK_STREAM
          SOCK_DGRAM

   套接字类型

.. data:: IPPROTO_UDP
          IPPROTO_TCP

IP协议号

.. data:: SOL_SOCKET

socket选项级别,默认=4095
