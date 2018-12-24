.. _mpython.py:

掌控板库
=========

.. module:: mpyhton

mpython是基于掌控板封装的专用库

延时
-------

.. method:: sleep(s)

秒级延时

    - ``s`` -单位秒。

.. method:: sleep_ms(ms)

毫秒级延时

    - ``ms`` -单位毫秒。

.. method:: sleep_us(us)

级延时

    - ``us`` -单位微秒。


映射
-------

.. method:: numberMap(inputNum,bMin,bMax,cMin,cMax)

映射函数，参数：

- ``inputNum`` 为需要映射的变量

- ``bMin`` 为需要映射的最小值

- ``bMax`` 为需要映射的最大值

- ``cMin`` 为映射的最小值

- ``cMax`` 为映射的最大值



板载传感器
-------

声音、光线
+++++++++

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

bme280
-------

BME280是一款集成温度、湿度、气压，三位一体的环境传感器。具有高精度，多功能，小尺寸等特点。

* 温度检测范围：-40℃~+85℃，分辨率0.1℃，误差±0.5℃
* 湿度检测范围：0~100%RH，分辨率0.1%RH，误差±2%RH
* 压力检测范围：300~1100hPa
* 湿度测量响应时间：1s

.. Attention:: 

    掌控板预留BME280芯片位置未贴片,默认配置的掌控板是不带BME280环境传感器,需留意!

.. method:: bme280.temperature()

返回温度值,单位摄氏度。

.. method:: bme280.pressure()

返回大气压值,单位Pa。

.. method:: bme280.humidity()

返回环境湿度,单位%。


蜂鸣器
-------

通过buzz对象,驱动板载无源蜂鸣器。

.. method:: buzz.on(freq=500)

以设定的频率打开无源蜂鸣器，默认为500Hz

- ``freq`` -默认500Hz，0 < freq ≤ 78125

.. method:: buzz.freq(freq)

切换蜂鸣器频率

- ``freq`` -0 < freq ≤ 78125

.. method:: buzz.off()

停止驱动无源蜂鸣器


button_[a,b]对象
------
掌控板上的a,b按键。button_a/button_b 是 ``machine.Pin`` 衍生类，继承Pin的方法。更详细的使用方法请查阅 :ref:`machine.Pin<machine.Pin>`  。



.. method:: button_[a,b].value()

获取button_[a,b]按键引脚状态。引脚IO以上，当按键为未按下状态时value==1,按下状态时value==0。

::

    >>> button_a.value()
    >>> 1
    >>> button_a.value()
    >>> 0

.. _button.irq:

.. method:: button_[a,b].irq(handler=None, trigger=(Pin.IRQ_FALLING | Pin.IRQ_RISING), priority=1, wake=None)

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

::

    >>> from mpython import *
    >>> button_a.irq(trigger=Pin.IRQ_FALLING, handler=lambda p:print("button-a press！")) 


touchPad_[ ]对象
------
掌控板上共有6个触摸引脚分别touchPad_P/Y/T/H/O/N。

.. method:: touchPad_[P,Y,T,H,O,N].read()

返回触摸值

::

    >>> touchPad_P.read()
    >>> 523

rgb对象
-------
用于控制掌控板的3颗RGB ws2812灯珠。rgb对象为neopixel的衍生类，继承neopixel的方法。更多的使用方法请查阅 :ref:`neopixel<neopixel>` 。 

.. method:: rgb.write()

把数据写入RGB灯珠中。 

.. Hint::

    通过给rgb[n]列表赋值来写入RGB颜色值。如，rgb[0]=(50,0,0)

::

    from mpython import *

    rgb[0] = (255, 0, 0)  # 设置为红色，全亮度
    rgb[1] = (0, 128, 0)  # 设定为绿色，半亮度
    rgb[2] = (0, 0, 64)   # 设置为蓝色，四分之一亮度

    rgb.write()

.. method:: rgb.fill(rgb_buf)

填充所有LED像素。

.. _oled:

oled对象
-------
oled对象为framebuf的衍生类，继承framebuf的方法。更多的使用方法请查阅 :mod:`framebuf<framebuf>` 。 

.. method:: oled.poweron()

开启显示屏电源。

.. method:: oled.poweroff()

关闭显示器电源。

.. method:: oled.contrast(brightness)

设置显示屏亮度。

    - ``brightness`` 亮度,范围0~255


.. method:: oled.invert()

翻转像素点。当n=1时,未填充像素点点亮,填充像素点灭。当n=0时,则反。默认启动是填充像素点点亮。

.. method:: oled.DispChar(s, x, y)

oled屏显示文本。

    - ``s`` -需要显示的文本。
    - ``x`` 、``y`` -文本的左上角作为起点坐标。

.. method:: oled.show()

将frame缓存发送至oled显示。

::

    from mpython import *

    oled.DispChar('你好世界', 38, 0)
    oled.DispChar('hello,world', 32, 16)
    oled.DispChar('안녕하세요', 35, 32)
    oled.DispChar('こんにちは世界', 24, 48)
    oled.show()

.. method:: oled.fill(c)

        用指定的颜色填充整个帧缓存。 ``c`` 为1时,像素点亮；``c`` 为0时,像素点灭。

.. method:: oled.circle(x, y, radius , c)

绘制圆

    - ``x`` 、``y`` -左上角作为起点坐标。
    - ``radius`` -圆半径大小
    - ``c`` -为1时,像素点亮；``c`` 为0时,像素点灭。

.. method:: oled.fill_circle(x, y, radius , c)

绘制实心圆

    - ``x`` 、``y`` -左上角作为起点坐标。
    - ``radius`` -圆半径大小
    - ``c`` -为1时,像素点亮；``c`` 为0时,像素点灭。

.. method:: oled.triangle(x0, y0, x1, y1, x2, y2, c)

绘制三角形

    - ``x0`` 、``y0`` -三角形上顶点坐标 。
    - ``x1`` 、``y1`` -三角形左顶点坐标 。
    - ``x2`` 、``y2`` -三角形左顶点坐标 。
    - ``c`` -为1时,像素点亮；``c`` 为0时,像素点灭。

.. method:: oled.fill_triangle(x0, y0, x1, y1, x2, y2, c)

绘制实心三角形

    - ``x0`` 、``y0`` -三角形上顶点坐标 。
    - ``x1`` 、``y1`` -三角形左顶点坐标 。
    - ``x2`` 、``y2`` -三角形左顶点坐标 。
    - ``c`` -为1时,像素点亮；``c`` 为0时,像素点灭。


.. method:: oled.Bitmap(x, y, bitmap, w, h,c)

绘制bitmap图案

    - ``x`` 、``y`` -左上角作为起点坐标
    - ``bitmap`` -图案bitmap数组
    - ``w`` -图案宽度
    - ``h`` -图案高度
    - ``c`` -为1时,像素点亮；``c`` 为0时,像素点灭。


.. method:: oled.RoundRect( x, y, w, h, r, c)

绘制弧角矩形

    - ``x`` 、``y`` -左上角作为起点坐标
    - ``w`` -图案宽度
    - ``h`` -图案高度
    - ``r`` -圆弧角半径
    - ``c`` -为1时,像素点亮；``c`` 为0时,像素点灭。

MPythonPin类
-------

.. class:: MPythonPin(pin, mode=PinMode.IN,pull=None)

构建Pin对象

- ``pin`` 掌控板定义引脚号，具体定义看查看 :ref:`掌控板引脚定义<mpython_pinout>` 。

- ``mode`` 引脚模式，未设定时默认mode=PinMode

        - ``PinMode.IN`` 等于1，数字输入模式
        - ``PinMode.OUT`` 等于2，数字输出模式
        - ``PinMode.PWM`` 等于3，模拟输出模式
        - ``PinMode.ANALOG`` 等于4，模拟输入模式

- ``pull`` 指定引脚是否连接了电阻，可以是以下之一：

       - ``None`` - 无上拉或下拉电阻
       - ``Pin.PULL_UP`` - 上拉电阻使能
       - ``Pin.PULL_DOWN`` - 下拉电阻使能


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


.. _MPythonPin.irq:

.. method:: MPythonPin.irq(handler=None, trigger=Pin.IRQ_RISING):

如果引脚模式配置为 ``IN`` ,可配置该引脚的触发源处于活动状态时调用的中断处理程序。

参数:

     - ``handler`` 是一个可选的函数，在中断触发时调用。

     - ``trigger`` 配置可以触发中断的事件。可能的值是：

       - ``Pin.IRQ_FALLING`` 下降沿中断
       - ``Pin.IRQ_RISING`` 上升沿中断
       - ``Pin.IRQ_LOW_LEVEL`` 低电平中断
       - ``Pin.IRQ_HIGH_LEVEL`` 高电平中断

       这些值可以一起进行 ``OR`` 运算以触发多个事件。


Servo类
-------

.. class:: Servo(pin, min_us=750, max_us=2250, actuation_range=180)

构建Servo对象,默认使用SG90舵机。不同舵机脉冲宽度参数和角度范围会有所不一样,根据舵机型号自行设置。

.. Hint:: 

    作为Servo控制引脚须为支持PWM(模拟输出)的引脚。掌控板支持PWM的引脚,详情可查阅 :ref:`掌控板接口引脚说明<mPythonPindesc>` 。

.. Attention:: 

    * 你可以设置 ``actuation_range`` 来对应用给定的 ``min_us`` 和 ``max_us`` 观察到的实际运动范围值。
    * 您也可以将脉冲宽度扩展到这些限制之上和之下伺服机构可能会停止，嗡嗡声，并在停止时吸收额外的电流。仔细测试，找出安全的最小值和最大值。

- ``pin`` -舵机PWM控制信号引脚
- ``min_us`` -舵机PWM信号脉宽最小宽度,单位微秒。默认min_us=750
- ``max_us`` -舵机PWM信号脉宽最小宽度,单位微秒。默认max_us=2250
- ``actuation_range`` -舵机转动最大角度


.. method:: Servo.write_us(width)

发送设置脉冲宽度的PWM信号。

    - ``width`` -脉冲宽度,单位微秒。

.. method:: Servo.write_angle(angle)

写舵机角度

    - ``angle`` -舵机角度。


::

    from mpython import *

    s=Servo(0)

    while True:
            for i in range(0,180,1):
                    s.write_angle(i)
                    sleep_ms(50)
            for i in range(180,0,-1):
                    s.write_angle(i)
                    sleep_ms(50)


.. class:: UI

UI类
-------

提供UI界面类控件

.. class:: UI()

构建UI对象。

.. method:: UI.ProgressBar(x, y, width, height, progress)

绘制进度条。

    - ``x`` 、 ``y`` -左上角作为起点坐标
    - ``width`` -进度条宽度
    - ``height`` -进度条高度
    - ``progress`` -进度条百分比

::

    from mpython import *

    myUI=UI()
    myUI.ProgressBar(30,30,70,8,60)
    oled.show()

.. method:: UI.stripBar(x, y, width, height, progress,dir=1,frame=1)

绘制垂直或水平的柱状条

    - ``x`` 、 ``y`` -左上角作为起点坐标
    - ``width`` -柱状条宽度
    - ``height`` -柱状条高度
    - ``progress`` -柱状条百分比
    - ``dir`` -柱状条方向。dir=1时水平方向,dir=0时,垂直方向。
    - ``frame`` -当frame=1时,显示外框；当frame=0时,不显示外框。

Clock类
+++++

提供模拟钟表显示功能

.. class:: UI.Clock(x,y,radius)

构建Clock对象。

    - ``x`` 、``y`` -左上角作为起点坐标
    - ``radius`` -钟表半径


.. method:: UI.settime()

获取本地时间并设置模拟钟表时间


.. method:: UI.drawClock()

绘制钟表

.. method:: UI.clear()

清除钟表

::

    from mpython import*
    from machine import Timer
    import time


    clock=UI.Clock(64,32,30)

    def Refresh():
            clock.settime()
            clock.drawClock()
            oled.show()
            clock.clear()
    
    tim1 = Timer(1)

    tim1.init(period=1000, mode=Timer.PERIODIC, callback=lambda _:Refresh()) 

.. _mpython.wifi:

wifi类
------

提供便捷的wifi连接网络方式或热点wifi功能

.. class:: wifi()

构建wifi对象并会创建 ``sta`` 对象和 ``ap`` 对象。可参见 :mod:`network` 模块了解更多使用方法。

    - sta用于客户端连接路由器来连接网络。
    - ap用于掌控板作为热点接入方式。

.. method:: wifi.connectWiFi(ssid,password)

连接wifi网络

    - ``ssid`` -WiFi网络名称
    - ``password`` -WiFi密码

.. method:: wifi.disconnectWiFi()

断开wifi网络连接

.. method:: wifi.enable_APWiFi(essid,channel)

开启wifi网络热点

 - ``essid`` - 创建热点的WiFi网络名称
 - ``channel`` -设置wifi使用信道,channel 1~13

.. method:: wifi.disable_APWiFi()

关闭wifi网络热点

DHT11类
------

提供了dht11温湿度传感器读取相关的函数。

构建对象
~~~~~~~
.. class:: DHT11(pin)

创建一个与引脚pin相连的DHT22传感器对象。

- ``pin``:引脚



方法
~~~~~~~

.. method:: DHT11.humidity()

读取并返回传感器的湿度值。 

.. method:: DHT11.temperature()

读取并返回传感器的温度值。  


DHT22类
------

同DHT11类,此处不再重复。