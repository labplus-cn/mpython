.. _micropython_lib:

MicroPython 库
=====================

.. warning::

   本节的重要摘要

   * MicroPython为每个模块实现了Python功能的子集。
   * 为了简化可扩展性，MicroPython版本的标准Python模块通常具有``u``（“micro”）前缀。
   * 任何特定的MicroPython变体或端口可能会遗漏本通用文档中描述的任何功能/功能（由于资源限制或其他限制）。

本章介绍了MicroPython中内置的模块（函数和类库）。这类模块有几类：

* 实现标准Python功能子集的模块，不应由用户扩展。
* 实现Python功能子集的模块，由用户提供扩展（通过Python代码）。
* 实现Python标准库的MicroPython扩展的模块。
* 特定于特定 :term:`MicroPython port` 的模块，因此不可移植。 

关于模块及其内容的可用性的注意事项：本文档通常希望描述在MicroPython项目
中实现的所有模块和函数/类。但是，MicroPython具有高度可配置性，
每个特定电路板/嵌入式系统的端口仅提供MicroPython库的子集。
对于官方支持的端口，需要过滤掉不适用的项目，或使用“可用性：”
子句标记单个描述，这些子句描述哪些端口提供给定功能。


记住这一点，请仍然注意，本文描述的模块(甚至整个模块)中的一些函数/类 
**可能** 在特定系统上的MicroPython的特定构建中 **不可用** 。
查找特定特性的可用性/不可用性的一般信息的最佳位置是“通用信息”部分，
其中包含与特定 :term:`MicroPython port` 端口相关的信息。

在一些端口上，您可以发现可用的内置库，可以通过在REPL中输入以下内容来导入::

    >>> help('modules')


除了本文档中描述的内置库之外，在 :term:`micropython-lib`  中还可以找到来自Python标准库的更多模块以及对它的进一步微Python扩展。



Python 标准库 和 micro-库
---------------------------------------------

以下标准Python库已经“微观化”以适应MicroPython的理念。它们提供该模块的核心功能，旨在成为标准Python库的直接替代品。
下面的一些模块使用标准的Python名称，但前缀为“u”，例如 ``ujson`` 代替 ``json`` 。这表示这样的模块是微库，即仅实现CPython模块功能的子集。
通过不同地命名它们，用户可以选择编写Python级模块来扩展功能，以便更好地与CPython兼容（实际上，这是 :term:`micropython-lib` 上面提到的项目所做的）。

在某些嵌入式平台上，添加Python级包装器模块以实现与CPython的命名兼容性可能很麻烦，微模块既可以使用u-name，也可以使用非u-name。
可以通过库路径（ ``sys.path`` ）中的该名称文件覆盖非u名称。例如，首先搜索文件（或包目录）并加载该模块（如果找到）。
如果找不到任何内容，它将回退到加载内置模块。 ``import json`` ``json.py`` ``json`` ``ujson`` 



 .. toctree::
      :maxdepth: 1

      builtins.rst
      array.rst
      gc.rst
      math.rst
      sys.rst
      ubinascii.rst
      ucollections.rst
      uerrno.rst
      uhashlib.rst
      uheapq.rst
      uio.rst
      ujson.rst
      uos.rst
      ure.rst
      uselect.rst
      usocket.rst
      ussl.rst
      ustruct.rst
      utime.rst
      uzlib.rst


      


MicroPython-ESP32专有库
------------------------------

以下库中提供了特定于MicroPython-ESP32实现的功能。


.. toctree::
   :maxdepth: 1

   btree.rst
   framebuf.rst
   machine.rst
   network.rst
   uctypes.rst
   micropython.rst