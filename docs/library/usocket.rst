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
  - ``type`` ：类型
  - ``proto`` ：协议号


一般不指定proto参数，因为有些MicroPython固件提供默认参数::

  >>> s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  >>> print(s)
  <socket>

.. function:: getaddrinfo(host, port)

将主机域名（host）和端口（port）转换为用于创建套接字的5元组序列。元组列表的结构如下::

  (family, type, proto, canonname, sockaddr)

下面显示了怎样连接到一个网址:：

  s = usocket.socket()
  s.connect(usocket.getaddrinfo('www.micropython.org', 80)[0][-1])

.. admonition:: 与CPython区别
  :class: attention

  CPython raises a ``socket.gaierror`` exception (`OSError` subclass) in case
  of error in this function. MicroPython doesn't have ``socket.gaierror``
  and raises OSError directly. Note that error numbers of `getaddrinfo()`
  form a separate namespace and may not match error numbers from
  `uerrno` module. To distinguish `getaddrinfo()` errors, they are
  represented by negative numbers, whereas standard system errors are
  positive numbers (error numbers are accessible using ``e.args[0]`` property
  from an exception object). The use of negative values is a provisional
  detail which may change in the future.

  该函数发生错误时，会引发一个 ``socket.gaierror`` 异常（ ``OSError`` 子类）。 
  MicroPython并不具有 ``socket.gaierror`` ，会直接引发OSError。 
  注意： ``getaddrinfo()`` 的错误数量组成一个单独的名称空间，
  可能与 ``uerrno`` 系统错误代码模块中的错误数量不匹配。
   为区分 ``getaddrinfo()`` 错误，该错误使用负数标记，标准系统错误为正数（错误数可通过使用异常对象的 e.args[0] 特性访问）。
   暂时使用负数，未来可能改变。


常数
---------

地址簇
++++++

.. data:: AF_INET

等于2,TCP/IP – IPv4

.. data:: AF_INET6

等于10,TCP/IP – IPv6


socket类型
++++++




.. data:: SOCK_STREAM 等于1 — TCP流

.. data:: SOCK_DGRAM

等于2 — UDP数据报

.. data:: SOCK_RAW 

等于3 — 原始套接字

.. data:: SO_REUSEADDR  

等于4 — socket可重用

IP协议号
+++++++

.. data:: IPPROTO_UDP

默认值为16

.. data:: IPPROTO_TCP

默认值为17

socket选项级别
++++++++++

.. data:: SOL_SOCKET 

默认值为4095


class socket
============

Methods
-------

.. method:: socket.close()

   Mark the socket closed and release all resources. Once that happens, all future operations
   on the socket object will fail. The remote end will receive EOF indication if
   supported by protocol.

   Sockets are automatically closed when they are garbage-collected, but it is recommended 
   to `close()` them explicitly as soon you finished working with them.

.. method:: socket.bind(address)

   Bind the socket to *address*. The socket must not already be bound.

.. method:: socket.listen([backlog])

   Enable a server to accept connections. If *backlog* is specified, it must be at least 0
   (if it's lower, it will be set to 0); and specifies the number of unaccepted connections
   that the system will allow before refusing new connections. If not specified, a default
   reasonable value is chosen.

.. method:: socket.accept()

   Accept a connection. The socket must be bound to an address and listening for connections.
   The return value is a pair (conn, address) where conn is a new socket object usable to send
   and receive data on the connection, and address is the address bound to the socket on the
   other end of the connection.

.. method:: socket.connect(address)

   Connect to a remote socket at *address*.

.. method:: socket.send(bytes)

   Send data to the socket. The socket must be connected to a remote socket.
   Returns number of bytes sent, which may be smaller than the length of data
   ("short write").

.. method:: socket.sendall(bytes)

   Send all data to the socket. The socket must be connected to a remote socket.
   Unlike `send()`, this method will try to send all of data, by sending data
   chunk by chunk consecutively.

   The behavior of this method on non-blocking sockets is undefined. Due to this,
   on MicroPython, it's recommended to use `write()` method instead, which
   has the same "no short writes" policy for blocking sockets, and will return
   number of bytes sent on non-blocking sockets.

.. method:: socket.recv(bufsize)

   Receive data from the socket. The return value is a bytes object representing the data
   received. The maximum amount of data to be received at once is specified by bufsize.

.. method:: socket.sendto(bytes, address)

   Send data to the socket. The socket should not be connected to a remote socket, since the
   destination socket is specified by *address*.

.. method:: socket.recvfrom(bufsize)

  Receive data from the socket. The return value is a pair *(bytes, address)* where *bytes* is a
  bytes object representing the data received and *address* is the address of the socket sending
  the data.

.. method:: socket.setsockopt(level, optname, value)

   Set the value of the given socket option. The needed symbolic constants are defined in the
   socket module (SO_* etc.). The *value* can be an integer or a bytes-like object representing
   a buffer.

.. method:: socket.settimeout(value)

   Set a timeout on blocking socket operations. The value argument can be a nonnegative floating
   point number expressing seconds, or None. If a non-zero value is given, subsequent socket operations
   will raise an `OSError` exception if the timeout period value has elapsed before the operation has
   completed. If zero is given, the socket is put in non-blocking mode. If None is given, the socket
   is put in blocking mode.

   .. admonition:: Difference to CPython
      :class: attention

      CPython raises a ``socket.timeout`` exception in case of timeout,
      which is an `OSError` subclass. MicroPython raises an OSError directly
      instead. If you use ``except OSError:`` to catch the exception,
      your code will work both in MicroPython and CPython.

.. method:: socket.setblocking(flag)

   Set blocking or non-blocking mode of the socket: if flag is false, the socket is set to non-blocking,
   else to blocking mode.

   This method is a shorthand for certain `settimeout()` calls:

   * ``sock.setblocking(True)`` is equivalent to ``sock.settimeout(None)``
   * ``sock.setblocking(False)`` is equivalent to ``sock.settimeout(0)``

.. method:: socket.makefile(mode='rb', buffering=0)

   Return a file object associated with the socket. The exact returned type depends on the arguments
   given to makefile(). The support is limited to binary modes only ('rb', 'wb', and 'rwb').
   CPython's arguments: *encoding*, *errors* and *newline* are not supported.

   .. admonition:: Difference to CPython
      :class: attention

      As MicroPython doesn't support buffered streams, values of *buffering*
      parameter is ignored and treated as if it was 0 (unbuffered).

   .. admonition:: Difference to CPython
      :class: attention

      Closing the file object returned by makefile() WILL close the
      original socket as well.

.. method:: socket.read([size])

   Read up to size bytes from the socket. Return a bytes object. If *size* is not given, it
   reads all data available from the socket until EOF; as such the method will not return until
   the socket is closed. This function tries to read as much data as
   requested (no "short reads"). This may be not possible with
   non-blocking socket though, and then less data will be returned.

.. method:: socket.readinto(buf[, nbytes])

   Read bytes into the *buf*.  If *nbytes* is specified then read at most
   that many bytes.  Otherwise, read at most *len(buf)* bytes. Just as
   `read()`, this method follows "no short reads" policy.

   Return value: number of bytes read and stored into *buf*.

.. method:: socket.readline()

   Read a line, ending in a newline character.

   Return value: the line read.

.. method:: socket.write(buf)

   Write the buffer of bytes to the socket. This function will try to
   write all data to a socket (no "short writes"). This may be not possible
   with a non-blocking socket though, and returned value will be less than
   the length of *buf*.

   Return value: number of bytes written.

.. exception:: usocket.error

   MicroPython does NOT have this exception.

   .. admonition:: Difference to CPython
        :class: attention

        CPython used to have a ``socket.error`` exception which is now deprecated,
        and is an alias of `OSError`. In MicroPython, use `OSError` directly.
