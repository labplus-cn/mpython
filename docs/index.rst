.. mPython掌控板 documentation master file, created by
   sphinx-quickstart on Tue Aug 28 17:25:35 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

mPython帮助文档
======================================

欢迎您，使用掌控板！

mPython掌控板是一块MicroPython微控制器板，它集成ESP32高性能双核芯片，使用当下最流行的Python编程语言，以便您轻松地将代码从电脑传输到掌控板中，从而体验程序创作的无穷乐趣！

.. image:: /images/掌控-动态.gif


| 掌控板官网: https://www.mpython.cn
| GitHub开源: https://github.com/labplus-cn/mPython
| mPython掌控板文档: https://mPython.readthedocs.io
| mPythonX IDE 软件编程文档: https://mPythonX.readthedocs.io
| Awesome-mPython(掌控资源大全) : https://labplus-cn.github.io/awesome-mpython/

.. Hint::

    我们已将掌控板项目的软硬件资源分享至GitHub，供各位掌控板爱好者学习阅览！

.. Attention::

     该项目正在积极开发中。由于ESP32仍然面向开发人员，并非所有外围设备都能完美使用，可能仍然存在一些bug，我们将会不断及时修复和更新。

---------

mPython掌控板资料
---------

.. toctree::
   :maxdepth: 2

   board/index.rst


---------

.. toctree::
   :maxdepth: 2
   :caption: 掌控板教程

   tutorials/basics/index.rst
   tutorials/advance/index.rst

---------

经典案例
++++++

.. toctree::
    :maxdepth: 2


    classic/index.rst

---------

MicroPython类库
----------------

.. toctree::
   :maxdepth: 1
   :caption: MicroPython类库
   :hidden:

   library/pythonStd/index.rst
   library/micropython/index.rst


=========================================   ======================================================
 :ref:`Python标准库<pythonStd>`               兼容CPython,内含Python内建函数、常用module
 :ref:`MicroPython类库<microPythonModu>`      MicroPython的ESP32硬件控制层的模块
=========================================   ======================================================


您可以通过 ``help()`` 发现可用的内置库，在REPL中输入以下内容来导入::

    >>> help('modules')


除了本文档中描述的内置库之外，在 :term:`micropython-lib`  中还可以找到来自Python标准库的更多模块以及对它的进一步微Python扩展。

---------

mPython类库
-------------

.. toctree::
   :maxdepth: 1
   :caption: mPython类库
   :hidden:

   library/mPython/index.rst

       
- :mod:`mpython`  --------- 掌控板板载相关功能函数                                
- :mod:`music` --------- 音乐相关功能函数,兼容micro:bit music 模块
- :mod:`urequests` --------- HTTP客户端的相关功能函数
- :mod:`umqtt.simple` --------- 简单MQTT客户端功能函数
- :mod:`gui` --------- GUI类的绘制元素
- :mod:`audio` --------- 音频播放录音
- :mod:`radio` --------- 无线广播
- :mod:`sdcard` --------- 挂载SD卡
- :mod:`bluebit` --------- blue:bit驱动
- :mod:`parrot` --------- 掌控拓展板驱动
- :mod:`ds18x20` --------- ds18b20温度传感器驱动




---------

.. toctree::
   :maxdepth: 1
   :caption: MicroPython 语法

   reference/index.rst

有关MicroPython特定语言功能的语言参考信息


.. toctree::
   :hidden:
   
   license.rst


.. toctree::
   :hidden:

   release.rst


掌控拓展板
----------

.. toctree::
   :hidden:

   extboard/index.rst

.. image:: /images/extboard/extboard_250.png
  :scale: 80 %
  :target: extboard/index.html


------------------

索引
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
