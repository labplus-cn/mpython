.. _servo:
:mod:`servo`

servo 模块
==========

Servo类
-------

.. class:: Servo(pin, min_us=750, max_us=2250, actuation_range=180)

构建Servo对象,默认使用SG90舵机。不同舵机脉冲宽度参数和角度范围会有所不一样,根据舵机型号自行设置。

.. Hint:: 

    作为Servo控制引脚须为支持PWM(模拟输出)的引脚。掌控板支持PWM的引脚,详情可查阅 :ref:`掌控板接口引脚说明<mPythonPindesc>` 。

.. Attention:: 

    * 你可以设置 ``actuation_range`` 来对应用给定的 ``min_us`` 和 ``max_us`` 观察到的实际运动范围值。
    * 您也可以将脉冲宽度扩展到这些限制之上和之下伺服机构可能会停止，嗡嗡声，并在停止时吸收额外的电流。仔细测试，找出安全的最小值和最大值。
    * 由于舵机PWM周期为20ms,即响应时间为20ms。在编程时须注意两次写舵机角度间隔时间应至少大于20ms。

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
    from servo import Servo                 #导入舵机模块

    s=Servo(0)

    while True:
            for i in range(0,180,1):
                    s.write_angle(i)
                    sleep_ms(50)
            for i in range(180,0,-1):
                    s.write_angle(i)
                    sleep_ms(50)
