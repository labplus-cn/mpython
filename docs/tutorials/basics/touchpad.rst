触摸按键
=======

在掌控板正面金手指处拓展6个触摸按键，依次P、Y、T、H、O、N。


------------------------------------------------------------

.. literalinclude:: /../examples/button/button_tp_ctl_rgb.py
    :caption: 示例-触摸不同按键，点亮不同色RGB灯
    :linenos:
        

首先导入 mpython模块，尝试用手指触摸P金手指处，使用 ``read()`` 读取值。观察变化::

  >>> from mpython import *
  >>> touchPad_P.read()
  643
  >>> touchPad_P.read()
  8

.. Note::

  掌控板板载6个触摸焊盘，依次从左到右分别touchPad_P、touchPad_Y、touchPad_T、touchPad_H、touchPad_O、touchPad_N，其他触摸按键使用方法同上。

.. image:: /images/掌控板引脚定义-正面.png