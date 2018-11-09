.. mPython掌控板 documentation master file, created by
   sphinx-quickstart on Tue Aug 28 17:25:35 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

mPython掌控板文档
======================================

欢迎您，使用掌控板！

mPython掌控板是一块MicroPython微控制器板，它集成ESP32高性能双核芯片，使用当下最流行的Python编程语言，以便您轻松地将代码从桌面传输到微控制器或嵌入式系统。

.. image:: /images/掌控-动态.gif



| GitHub: https://github.com/labplus-cn/mPython
| mPython掌控板在线文档: https://mPython.readthedocs.io

.. Hint::

    我们已将掌控项目的软硬件资源分享至GitHub，供各位掌控爱好者学习阅览！

.. Attention::

     该项目正在积极开发中。由于ESP32仍然面向开发人员。并非所有外围设备都能完美使用，可能仍然存在一些bug，我们将会不断及时更新并修复。

.. toctree::
   :maxdepth: 2
   :caption: mPython掌控板

   board/introduction.rst
   board/software.rst
   board/hardware.rst
   board/flashburn.rst

   
.. toctree::
   :maxdepth: 1
   :caption: 掌控板入门教程
   :numbered:

   tutorials/repl.rst
   tutorials/filesystem.rst
   tutorials/display.rst
   tutorials/buttons.rst
   tutorials/digital_io.rst
   tutorials/analog_io.rst
   tutorials/neopixel.rst
   tutorials/buzz.rst
   tutorials/sound&light.rst
   tutorials/accelerometer.rst
   tutorials/random.rst
   tutorials/i2c.rst
   tutorials/network/index.rst

.. toctree::
    :maxdepth: 1
    :caption: 进阶教程
        
    classic/oneNetCmd.rst
    classic/oneNetDatastreams.rst
    


mpython 库
-----------------

该库中提供了mPython掌控板特有拓展功能。
获取最新的 :download:`mpython.py </../examples/library/mpython.py>` 。

.. toctree::
   :maxdepth: 1

   library/mpython.rst
   
  

MicroPython 库
-----------------

.. toctree::
   :maxdepth: 3

   library/index.rst

 


本章介绍了MicroPython中内置的模块（函数和类库）。这类模块有几类：

* 实现标准Python功能子集的模块，不应由用户扩展。
* 实现Python功能子集的模块，由用户提供扩展（通过Python代码）。
* 实现Python标准库的MicroPython扩展的模块。
* 特定于特定 :term:`MicroPython port` 的模块，因此不可移植。 




.. toctree::
   :maxdepth: 1
   :caption: MicroPython 语法

   reference/index.rst
 
有关MicroPython特定语言功能的语言参考信息


索引
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
