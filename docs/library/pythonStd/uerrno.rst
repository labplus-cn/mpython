:mod:`uerrno` -- 系统错误代码
===================================

.. module:: uerrno
   :synopsis: 系统错误代码

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `errno <https://docs.python.org/3.5/library/errno.html#module-errno>`_

此模块提供访问符号错误代码以进行 :ref:`OSError <OSError>`  异常。特定的代码清单依赖于 :term:`MicroPython port`.


常量
---------

.. data:: EEXIST, EAGAIN, etc.

    错误代码，基于ANSI C/POSIX标准。所有错误代码开头都有“E”。错误通常可以访问为 ``exc.args[0]`` ，其中 ``exc`` 是 ``OSError`` 的一个实例

    示例::

        try:
            uos.mkdir("my_dir")
        except OSError as exc:
            if exc.args[0] == uerrno.EEXIST:
                print("Directory already exists")

.. data:: errorcode

    字典将数字错误代码映射到带有符号错误代码的字符串（参见上文）::

        >>> print(uerrno.errorcode[uerrno.EEXIST])
        EEXIST


===================================  ================  ====================================
异常                                  值                描述
``uerrno.EPERM``                      1                Operation not permitted
``uerrno.ENOENT``                     2                No such file or directory
``uerrno.ESRCH``                      3                No such process
``uerrno.EINTR``                      4                Interrupted system call
``uerrno.EIO``                        5                I/O error
``uerrno.ENXIO``                      6                No such device or address
``uerrno.E2BIG``                      7                Argument list too long
``uerrno.ENOEXEC``                    8                Exec format error
``uerrno.EBADF``                      9                Bad file number
``uerrno.ECHILD``                     10               No child processes
``uerrno.EAGAIN``                     11               Try again
``uerrno.ENOMEM``                     12               Out of memory
``uerrno.EACCES``                     13               Permission denied
``uerrno.EFAULT``                     14               Bad address
``uerrno.ENOTBLK``                    15               Block device required
``uerrno.EBUSY``                      16               Device or resource busy
``uerrno.EEXIST``                     17               File exists
``uerrno.EXDEV``                      18               Cross-device link
``uerrno.ENODEV``                     19               No such device
``uerrno.ENOTDIR``                    20               Not a directory
``uerrno.EISDIR``                     21               Is a directory
``uerrno.EINVAL``                     22               Invalid argument
``uerrno.ENFILE``                     23               File table overflow
``uerrno.EMFILE``                     24               Too many open files
``uerrno.ENOTTY``                     25               Not a typewriter
``uerrno.ETXTBSY``                    26               Text file busy
``uerrno.EFBIG``                      27               File too large
``uerrno.ENOSPC``                     28               No space left on device
``uerrno.ESPIPE``                     29               Illegal seek
``uerrno.EROFS``                      30               Read-only file system
``uerrno.EMLINK``                     31               Too many links
``uerrno.EPIPE``                      32               Broken pipe
``uerrno.EDOM``                       33               Math argument out of domain of func
``uerrno.ERANGE``                     34               Math result not representable
``uerrno.EWOULDBLOCK``                11               Operation would block
``uerrno.EOPNOTSUPP``                 95               Operation not supported on transport endpoint
``uerrno.EAFNOSUPPORT``               97               Address family not supported by protocol
``uerrno.EADDRINUSE``                 98               Address already in use
``uerrno.ECONNABORTED``               99               Software caused connection abort
``uerrno.ECONNRESET``                 104              Connection reset by peer
``uerrno.ENOBUFS``                    105              No buffer space available
``uerrno.EISCONN``                    106              Transport endpoint is already connected
``uerrno.ENOTCONN``                   107              Transport endpoint is not connected
``uerrno.ETIMEDOUT``                  110              Connection timed out
``uerrno.ECONNREFUSED``               111              Connection refused
``uerrno.EHOSTUNREACH``               113              No route to host
``uerrno.EALREADY``                   114              Operation already in progress
``uerrno.EINPROGRESS``                115              Operation now in progress
===================================  ================  ====================================