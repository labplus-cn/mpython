.. _pythonStd:

Python标准库
===========

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


      


