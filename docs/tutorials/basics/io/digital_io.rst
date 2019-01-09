数字IO
===============

本章节介绍了掌控板的I/O引脚的数字输入输出使用方法。引脚是掌控板与连接到它的外部设备进行通信的方式。掌控板可以通过拓展板将IO引脚拓展并连接控制或读取其他元器件或模块。

.. Attention:: 

    除P2(只限数字输入)P3,P4,P10以外,其他引脚均可是使用数字输入、输出模式。有关更详细说明,请查看 :ref:`掌控板接口引脚说明<mPythonPindesc>` 。


数字输入
------------------   

首先,从如何读取引脚的数字输入开始。以下使用掌控板内置的按键a,作为按键输入::

    from mpython import *           # 导入mpython模块

    p5=MPythonPin(5,PinMode.IN)     # 实例化MPythonPin,将按键a引脚(P5)设置为"PinMode.IN"模式

    while True:
        value=p5.read_digital()      # 读取P5引脚的数字输入
        oled.DispChar("Button_a:%d" %value,30,20)   # 将读取到值显示至oled上
        oled.show()                                  # 刷新
        oled.fill(0)                                 # 清屏

.. Note::

    这时,你可以按下button a按键看下“按下”和“未按下”的读值。由于按键a电路做了上拉,所以“未按下”时输出为高电平, “按下”时输出为低电平。
    
::

    from mpython import *
    p5=MPythonPin(5,PinMode.IN) 
    

使用前，请务必先将 mpython 模块导入，方可使用。

实例化引脚对象并设置模式。这里使用到 ``MPythonPin(pin, mode=PinMode.IN,pull=None)`` 类。
``pin`` 是您要访问的引脚。如果未指定mode，则默认为 ``PinMode.IN`` 。如果未指定pull，则默认为 ``None`` 。

::

    p5.read_digital()

.. Note:: 使用read_digital(),返回引脚的电平值。高电平(1),低电平(0)。


数字输出
------------------ 

以下是简单的驱动外部LED灯闪烁::

    from mpython import *           # 导入mpython模块

    p0=MPythonPin(0,PinMode.OUT)     # 实例化MPythonPin,将P0设置为"PinMode.OUT"模式

    while True:
        p0.write_digital(1)          # P0写高电平
        sleep(1)                     #  延时
        p0.write_digital(0)          # P0写高电平
        sleep(1)                     #  延时


.. admonition:: 材料、连接方式

    上面需要使用到一块面包板、1个LED灯、mPython拓展板、杜邦线。LED灯的正极连接至掌控板的P0引脚,LED负极连接至掌控板的GND。

.. image:: /images/tutorials/blink.gif

::

    p0=MPythonPin(0,PinMode.OUT)  


.. Note:: 

    ``MPythonPin`` 实例化。``mode`` 设置为 ``PinMode.OUT`` 数字输出模式。

对P0引脚写高低电平::

    p0.write_digital(1)
    p0.write_digital(0)

.. Note:: 

    使用 ``write_digital(value)`` 方法对引脚写高低电平。其中 ``value`` 是电平值,“1”代表高电平,“0”代表低电平。


外部中断
---------

.. admonition:: 什么是中断呢？

    在程序运行过程中，系统出现了一个必须由CPU立即处理的情况，此时，CPU暂时中止程序的执行转而处理这个新的情况的过程就叫做中断。
    在出现需要时，CPU必须暂停现在的事情，处理别的事情，处理完了再回去执行暂停的事情。

当输入引脚发生电平变化时触发硬件中断，触发器会执行中断处理函数。你可以定义回调函数来做中些断响应的工作。引脚中断使用和掌控板的a,b按键中断本质是一样的。

以下使用掌控板内置的按键a((P5引脚),作为输入中断,按下按键 A 时蜂鸣器发出声音::

    from mpython import *           # 导入mpython模块
    import music                    # 导入music模块
    p5=MPythonPin(5,PinMode.IN)     # 实例化MPythonPin,将P5设置为"PinMode.IN"模式

    def BuzzOn(_):                    # 定义中断的回调函数  
        music.play(music.BA_DING,wait=False)

    p5.irq(trigger=Pin.IRQ_FALLING,handler=BuzzOn)            # 设置P5引脚中断的回调函数

.. Hint:: 

    效果和时用 ``button_a.irq()`` 按键中断时一样的,button_a的中断也是使用到 ``Pin.irq`` 的方法。


我们首先实例化MPythonPin,将P5引脚配置为 ``PinMode.IN`` ::

    p5=MPythonPin(5,PinMode.IN) 

定义回调函数::

    def BuzzOn(_):                  
        music.play(music.BA_DING,wait=False)

.. Note:: 

   回调函数，**必须包含一个参数**,否则无法使用, 上面 ``BuzzOn()`` 定义回调函数,参数为 ``_``,你可以任意定义该参数。  


最后我们需要告诉引脚何时触发，以及在检测到事件时调用的函数::

    p5.irq(trigger=Pin.IRQ_FALLING,handler=BuzzOn)

.. Note::

    我们将P5设置为仅在下降沿触发  ``Pin.IRQ_FALLING`` （当它从高电平变为低电平时）。设置回调函数
    handler="你定义中断处理的回调函数"。更详细的触发方式，请查阅 :ref:`MPythonPin.irq <MPythonPin.irq>` 。


