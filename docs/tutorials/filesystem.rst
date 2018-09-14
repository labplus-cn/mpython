内部文件系统
=======================

文件系统为FAT格式。

文件的创建、读写
--------------------------

mPython支持 :term:`CPython` 中的内置的 ``open()`` 访问文件。

请尝试创建文件::

    >>> f = open('data.txt', 'w')
    >>> f.write('some data')
    9
    >>> f.close()

“9”是使用该write()方法写入的字节数。然后，您可以使用以下方法回读此新文件的内容::

    >>> f = open('data.txt')
    >>> f.read()
    'some data'
    >>> f.close()

请注意，打开文件时的默认模式是以 **只读模式** 打开它，并将其作为文本文件打开。
第二个参数为 ``wb`` 打开文件便是以二进制模式写入， ``rb`` 是以二进制模式读取。

.. Hint::

  有关更多的open()使用，可查阅 :term:`CPython` 文档:`open() <https://docs.python.org/3.5/library/functions.html#open>`_。



目录操作
---------------------

:mod:`os` 模块有更多的文件目录操作。

首先，import 模块::

    >>> import os

然后，列出当前目录文件::

    >>> os.listdir()
    ['boot.py', 'port_config.py', 'data.txt']

你可以创建目录::

    >>> os.mkdir('dir')

删除文件::

    >>> os.remove('data.txt')

启动脚本
----------------

boot.py和main.py，这两个文件在启动时由MicroPython专门处理。 首先执行boot.py脚本（如果存在），然后在完成后执行main.py脚本。



