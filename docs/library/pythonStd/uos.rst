:mod:`os` -- 基本的操作系统
===============================================

.. module:: os
   :synopsis: 操作系统

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `os <https://docs.python.org/3.5/library/os.html#module-os>`_

该uos模块包含文件系统访问和安装，终端重定向和复制 ``uname`` 以及 ``urandom`` 功能的功能。

一般功能
---------

.. function:: uname()

返回一个元组(可能是一个命名元组)，其中包含关于底层和/或其操作系统的信息。元组有五个字段，每个字段的顺序如下:

  * ``sysname`` -- 底层系统的名称
  * ``nodename`` -- 网络名称（和sysname相同）
  * ``release`` -- 底层系统的版本
  * ``version`` -- MiroPython版本和构建日期
  * ``machine`` --  底层硬件的标识符(eg board, CPU)

示例::

  >>> import os
  >>> os.uname()
  (sysname='esp32', nodename='esp32', release='1.9.1', version='v1.9.1-224-g83d3f3f-dirty on 2017-12-12', machine='ESP32 module with ESP32')


.. function:: urandom(n)

返回一个带有n个随机字节的字节对象。它是由硬件随机数生成器生成。

示例::

  >>> os.urandom(20)
  b'f\x92\x85t28\xa1\xf0\xaf3\xf5\xd9\xcdx\xc3\n\xedm\xf8\xb7'


文件系统访问
---------

.. function:: getcwd()

获取当前目录。

.. function:: chdir(path)

更改当前目录。

示例::

  >>> os.getcwd()
  '/'
  >>> os.chdir("./lib")
  >>> os.getcwd()
  '/lib'
  >>> os.chdir("..")
  >>> os.getcwd()
  '/'


.. function:: ilistdir([dir])

此函数返回一个迭代器，然后生成与列出的目录中的条目对应的元组。没有参数，它列出了当前目录，否则它列出了dir给出的目录。

The 3-tuples have the form *(name, type, inode)*:

  - *name* 是一个字符串（如果dir是一个字节对象，则为字节），并且是条目的名称;
  - *type* 是一个整数，指定条目的类型，目录为0x4000，常规文件为0x8000;
  - *inode* 是对应于文件inode的整数，对于没有这种概念的文件系统可以是0。

目前条目的含义目前尚未定义。

.. function:: listdir([dir])

如果没有参数，请列出当前目录。否则列出给定目录。

示例::
  >>> os.listdir()
  ['boot.py', 'lib']
  >>> os.listdir("./lib")
  ['test.py']


.. function:: mkdir(path)

创建目录，path为创建目录的路径。 

示例::

  >>> os.listdir()
  ['boot.py']
  >>> path = "./lib"
  >>> os.mkdir(path)
  >>> os.listdir()
  ['boot.py', 'lib']

.. function:: rmdir(path)

删除目录。

示例::

  >>> os.listdir()
  ['boot.py', 'lib']
  >>> os.rmdir("./lib")
  >>> os.listdir()
  ['boot.py']


.. function:: remove(path)

删除文件。 

示例::

  >>> os.listdir("./lib")
  ['test.py']
  >>> os.remove("./lib/test.py")
  >>> os.listdir("./lib")
  []



.. function:: rename(old_path, new_path)

重命名文件。 

示例::

  >>> os.listdir(os.getcwd())
  ['test.py']
  >>> os.rename("test.py", "mytest.py")
  >>> os.listdir(os.getcwd())
  ['mytest.py']


.. function:: stat(path)

获取文件或目录的状态。 

示例::

  >>> os.stat("./lib")
  (16384, 0, 0, 0, 0, 0, 0, 0, 0, 0)
  >>> os.stat("./lib/test.py")
  (32768, 0, 0, 0, 0, 0, 1, 0, 0, 0)

.. function:: statvfs(path)

获取文件系统的状态。

返回包含以下顺序的文件系统信息的元组：

  * ``f_bsize`` -- 文件系统块大小
  * ``f_frsize`` -- 片段大小
  * ``f_blocks`` --  f_frsize单位的fs大小
  * ``f_bfree`` -- free blocks数量
  * ``f_bavail`` -- number of free blocks for unpriviliged users
  * ``f_files`` -- inodes数量
  * ``f_ffree`` -- number of free inodes
  * ``f_favail`` -- number of free inodes for unpriviliged users
  * ``f_flag`` -- mount flags
  * ``f_namemax`` -- 最大文件名长度

相关信息节点参数： ``f_files`` ，``f_ffree`` ，``f_avail`` 和 ``f_flags`` 参数可能会返回0。

.. function:: sync()

同步所有文件系统。

终端重定向和复制
---------------

.. function:: dupterm(stream_object, index=0)

复制或切换给定类似 ``stream`` 对象上的MicroPython终端（REPL）。所述 `stream_object` 参数必须是一个本地流对象，或从导出 ``uio.IOBase`` 并实施 ``readinto()`` 和 ``write()`` 方法。流应处于非阻塞模式，如果没有可用于读取的数据， ``readinto()`` 则应返回 ``None``。

调用此函数后，将在此流上重复所有终端输出，并且流上可用的任何输入都将传递到终端输入。

所述索引参数应该是哪个复制时隙设置一个非负整数，并且指定。给定端口可以实现多个槽（槽0将始终可用），并且在这种情况下，终端输入和输出在所有设置的槽上复制。

如果 ``None`` 作为 `stream_object` 传递，则在索引给出的槽上取消复制。

该函数返回给定槽中的前一个类似流的对象。


文件系统安装
----------

提供虚拟文件系统（VFS）以及在此VFS中安装多个“真实”文件系统的功能。文件系统对象可以安装在VFS的根目录中，也可以安装在根目录中的子目录中。
这允许Python程序看到的文件系统的动态和灵活配置。提供 ``mount()`` 和 ``umount()`` 功能，以及可能由VFS类表示的各种文件系统实现。


.. function:: mount(fsobj, mount_point, \*, readonly)

    将文件系统对象 `fsobj` 挂载到mount_point字符串指定的VFS中的位置。 
    fsobj可以是具有 ``mount()`` 方法或块设备的VFS对象。如果它是块设备，则会自动检测文件系统类型（如果未识别文件系统，则会引发异常）。
    `mount_point` 可以是在根目录下'/'挂载 `fsobj` ，也'/<name>'可以将它挂载在根目录下的子目录中。

如果是 `readonly` 为 `True` 则文件系统以只读方式挂载。

在挂载过程中，将 ``mount()`` 在文件系统对象上调用该方法。

``OSError(EPERM)`` 如果 `mount_point` 已经安装，则会引发。

.. function:: umount(mount_point)

    卸载文件系统。`mount_point` 可以是命名安装位置的字符串，也可以是先前安装的文件系统对象。在卸载过程中，将 `umount()` 在文件系统对象上调用该方法。

``OSError(EINVAL)`` 如果找不到 `mount_point` ，则会引发。

.. class:: VfsFat(block_dev)

    创建使用 `FAT` 文件系统格式的文件系统对象。FAT文件系统的存储由 `block_dev` 提供。可以使用此构造函数创建的对象 ``mount()`` 。

    .. staticmethod:: mkfs(block_dev)

        在 `block_dev` 上构建FAT文件系统。

