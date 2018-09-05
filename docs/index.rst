.. handPy掌控 documentation master file, created by
   sphinx-quickstart on Tue Aug 28 17:25:35 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

handPy掌控11112
======================================

MicroPython是Python 3编程语言的精简高效实现 ，包括Python标准库的一小部分，并且经过优化，可在微控制器和受限环境中运行。

handPy掌控是一块MicroPython微控制器板。专为物联网设计，板载ESP-WROOM-32双核芯片，支持WiFi和蓝牙双模通信。 板上集成5x5 RGB点阵/OLED、加速度计、气象传感器(含温湿度气压)、声、光传感器、蜂鸣器、4个物理按键、4个触摸按键。
除此外，还有一个阻性输入接口，方便接入各种阻性传感器。丰富多样的传感器和小体积的尺寸、结合蓝牙和WiFi双无线通讯，可现实不同的物联网应用场景。

MicroPython包含许多高级功能，如交互式提示，任意精度整数，闭包，列表理解，生成器，异常处理等。然而它非常紧凑，可以在仅256k的代码空间和16k的RAM内运行。

MicroPython旨在尽可能与普通Python兼容，以便您轻松地将代码从桌面传输到微控制器或嵌入式系统。

.. image:: images/handPy.gif   


.. toctree::
   :maxdepth: 2
   :caption: handPy

   inc/introduction.rst

   
.. toctree::
   :maxdepth: 2
   :caption: handPy快速入门教程

   tutorials/class1.rst
   tutorials/class2.rst
   tutorials/class3.rst
   tutorials/class4.rst
   
  

MicroPython 库
-----------------

.. toctree::
   :maxdepth: 2

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
