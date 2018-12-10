教程标题
=======

简单介绍下本章教程学习内容。

二级标题
-------

简单的指令和单功能点，几条指令可以完成的，首先采用repl方式来教学。像一些比较复杂的应用类的示例，应附上完整的示例。
每个知识点学习完后，应有个简单示例结合上文的知识点！

repl示例::

    >>> from mpython import *
    >>> buzz.on()
    >>> buzz.on(1000)
    >>> buzz.off()
    >>>

完成示例::

    from mpython import *

    s=Servo(0)
    while True:
        for i in range(0,180,1):
            s.write_angle(i)
            print(i)
            sleep_ms(50)
        for i in range(180,0,-1):
            s.write_angle(i)
            print(i)
            sleep_ms(50)

.. Note::

    注解提示框：每步骤应有详细的语法或者函数说明！



二级标题
-------

标题有一个由七位ASCII码编码的可打印非字母数字字符组成的下划线（或上划线加下划线）。推荐选择的字符有：“= - ‘ : ’ " ~ ^ _ * + # < >”。

reStructuredText语法
::::::::

图片插入，gif的动态图也可以。

.. image:: /images/掌控-立2.png

提供本地项目内下载方式

:download:`mPython掌控板V0.9原理图 </../docs/hardware/labplus_mPython_V0.9.pdf>`

*斜体* 

**加粗** 

* 列表1
* 列表2

提示框
+++++++

.. Note:: 注解

.. Attention:: 注意

.. Hint:: 提示

.. Important:: 重要

.. Tip:: 小技巧

.. Caution:: 警告

.. admonition:: 自定义提示框

    自定义


