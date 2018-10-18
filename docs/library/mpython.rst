:mod:`mpython` --- 掌控板
=============================================

.. module:: mpython
   :synopsis: mpython专有库

button_a/b类
------
掌控板上的a,b按键。button_a/button_b 是 ``machine.Pin`` 衍生类，继承Pin的方法。

.. Hint::

  更详细的使用方法请查阅 :ref:`machine.Pin<machine.Pin>` 

.. method:: button_[a/b].value([x])

获取button_a/b按键引脚状态。引脚IO以上，当按键为未按下状态时value==1,按下状态时value==0。

.. method:: button_[].irq(handler=None, trigger=(Pin.IRQ_FALLING | Pin.IRQ_RISING), priority=1, wake=None)

配置在引脚的触发源处于活动状态时调用的中断处理程序。

touchPad_[ ]类
------
掌控板上共有6个触摸引脚分别touchPad_P/Y/T/H/O/N。

.. method:: touchPad_[ ].read()

返回触摸值

rgb类
-------
用于控制掌控板的3颗RGB ws2812灯珠。rgb类为neopixel的衍生类，继承neopixel的方法。更详细的使用方法请查阅 :ref:`neopixel<neopixel>` 。 

.. method:: rgb.write()

把数据写入RGB灯珠中。 

.. Hint::

  通过给rgb[n]列表赋值来写入RGB颜色值。如，rgb[0]=(50,0,0)

.. method:: rgb.fill(rgb_buf)

填充所有LED像素。

display类
-------

