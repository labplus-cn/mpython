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

标准的Python库被 “微型化”后，就是micropython标准库。它们仅仅提供了该模块的核心功能。一些模块没有直接使用标准的Python的名字，而是冠以"u"，例如 ``ujson`` 代替 ``json`` 。也就是说micropython标准库（=微型库），只实现了一部分模块功能。
通过他们的名字不同，用户有选择的去写一个Python级模块扩展功能，也是为实现更好的兼容性。（实际上，这是 :term:`micropython-lib` 上面提到的项目所做的）。

在嵌入式平台上，可添加Python级别封装库从而实现命名兼容CPython，微模块即可调用他们的u-name，也可以调用non-u-name。
根据non-u-name包路径的文件可重写。

例如，``import json`` 的话，首先搜索一个 ``json.py`` 文件或 ``json`` 目录进行加载。
如果没有找到，它回退到加载内置 ``ujson`` 模块。



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
   machine/machine.rst
   network.rst
   uctypes.rst
   micropython.rst
   neopixel.rst
   random.rst
   dht.rst

