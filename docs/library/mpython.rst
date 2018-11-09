:mod:`mpython` --- 掌控板库
=============================================

.. module:: 

基于掌控板封装的专用库

button_a/b对象
------
掌控板上的a,b按键。button_a/button_b 是 ``machine.Pin`` 衍生类，继承Pin的方法。

.. Hint::

  更详细的使用方法请查阅 :ref:`machine.Pin<machine.Pin>` 

.. method:: button_[a/b].value([x])

获取button_a/b按键引脚状态。引脚IO以上，当按键为未按下状态时value==1,按下状态时value==0。

.. method:: button_[].irq(handler=None, trigger=(Pin.IRQ_FALLING | Pin.IRQ_RISING), priority=1, wake=None)

配置在引脚的触发源处于活动状态时调用的中断处理程序。

参数:

     - ``handler`` 是一个可选的函数，在中断触发时调用。

     - ``trigger`` 配置可以触发中断的事件。可能的值是：

       - ``Pin.IRQ_FALLING`` 下降沿中断
       - ``Pin.IRQ_RISING`` 上升沿中断
       - ``Pin.IRQ_LOW_LEVEL`` 低电平中断
       - ``Pin.IRQ_HIGH_LEVEL`` 高电平中断

       这些值可以一起进行 ``OR`` 运算以触发多个事件。

     - ``priority`` 设置中断的优先级。它可以采用的值是特定于端口的，但是更高的值总是代表更高的优先级。

     - ``wake`` 选择此中断可唤醒系统的电源模式。它可以是 ``machine.IDLE`` ， ``machine.SLEEP`` 或 ``machine.DEEPSLEEP`` 。
     这些值也可以进行 ``OR`` 运算，使引脚在多种功耗模式下产生中断。

此方法返回一个回调对象。

touchPad_[ ]对象
------
掌控板上共有6个触摸引脚分别touchPad_P/Y/T/H/O/N。

.. method:: touchPad_[ ].read()

返回触摸值

rgb对象
-------
用于控制掌控板的3颗RGB ws2812灯珠。rgb对象为neopixel的衍生类，继承neopixel的方法。更多的使用方法请查阅 :ref:`neopixel<neopixel>` 。 

.. method:: rgb.write()

把数据写入RGB灯珠中。 

.. Hint::

  通过给rgb[n]列表赋值来写入RGB颜色值。如，rgb[0]=(50,0,0)

.. method:: rgb.fill(rgb_buf)

填充所有LED像素。

display对象
-------
display对象为framebuf的衍生类，继承framebuf的方法。更多的使用方法请查阅 :mod:`framebuf<framebuf>` 。 

.. method:: display.DispChar(s, x, y)

oled屏显示文本。

- ``s`` 需要显示的文本
- ``x`` 、``y`` 文本的左上角作为起点坐标。

.. method:: display.show()

.. method:: display.fill(c)

    用指定的颜色填充整个帧缓存。 ``c`` 为1时,像素点亮；``c`` 为1时,像素点灭。

MPythonPin类
-------

.. class:: MPythonPin(pin, mode=PinMode)

构建Pin对象

- ``pin`` 掌控板定义引脚号，具体定义看查看 :ref:`掌控板引脚定义<mpython_pinout>` 。

- ``mode`` 引脚模式，未设定时默认mode=PinMode

    - ``PinMode.IN`` 等于1，数字输入模式
    - ``PinMode.OUT`` 等于2，数字输出模式
    - ``PinMode.PWM`` 等于3，模拟输出模式
    - ``PinMode.ANALOG`` 等于4，模拟输入模式

示例::

    >>> from mpython import MPythonPin       #导入MPython模块
    >>> P0=MPythonPin(0,PinMode.IN)          #构建引脚0对象，设置数字输入模式



.. method:: MPythonPin.read_digital()

返回该IO引脚电平值。1代表高电平，0代表低电平

.. method:: MPythonPin.write_digital(value)

IO引脚输出电平控制。``value`` =1时输出高电平， ``value`` =0时输出低电平。

.. method:: MPythonPin.read_analog()

读取ADC并返回读取结果，返回的值将在0到4095之间。

.. method:: MPythonPin.write_analog(duty, freq=1000):

设置输出PWM信号的占空比。

- ``duty`` 0 ≤ duty ≤ 1023
- ``freq`` PWM波频率,0 < freq ≤ 0x0001312D（十进制：0 < freq ≤ 78125）

板载传感器
-------

声音、光线
+++++++++

light、sound对象为ADC的衍生类，继承ADC的方法。更多的使用方法请查阅 :ref:`machine.ADC<machine.ADC>` 。

.. method:: light.read()

读取板载光线传感器值，范围0~4095。


.. method:: sound.read()

读取板载麦克风，范围0~4095。

加速度计
+++++++++

通过accelerometer对象，您可以获取3轴加速度计值，单位g，范围-2~+2g。

.. method:: accelerometer.get_x()

获取x轴上的加速度测量值，正整数或负整数，具体取决于方向。

.. method:: accelerometer.get_y()

获取y轴上的加速度测量值，正整数或负整数，具体取决于方向。

.. method:: accelerometer.get_z()

获取z轴上的加速度测量值，正整数或负整数，具体取决于方向。

蜂鸣器
-------

通过buzz对象,驱动板载无源蜂鸣器。

.. method:: buzz.on(freq=500)

以设定的频率打开无源蜂鸣器，默认为500Hz

- ``freq`` 默认500Hz，0 < freq ≤ 78125

.. method:: buzz.freq(freq)

切换蜂鸣器频率

- ``freq`` 0 < freq ≤ 78125

.. method:: buzz.off()

停止驱动无源蜂鸣器



