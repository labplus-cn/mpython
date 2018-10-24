.. currentmodule:: machine
.. _machine.PWM:

类 PWM -- 脉冲宽度调制
=============================

脉冲宽度调制（PWM）是一种通过数字方式获取模拟结果的技术。


构建对象
------------

.. class:: PWM(pin, freq, duty)

创建与设定引脚关联的PWM对象。这样您就可以写该引脚上的模拟值。

 - ``pin`` 支持PWM的引脚  ``GPIO0``、``GPIO2``、``GPIO4``、``GPIO5``、``GPIO10``、``GPIO12~19``、``GPIO21``、``GPIO22``、``GPIO23``、``GPIO25~27``。详见 `ESP32引脚功能表. <../../../images/pinout_wroom_pinout.png>`_ 
 - ``freq`` 频率,0 < freq <= 78125
 - ``duty``  占空比, 0 ≤ duty ≤ 0x03FF (十进制：0 ≤ duty ≤ 1023)


示例::

  from machine import PWM, Pin

  pwm = PWM (Pin(2), freq=1000,  duty=1023)    # create an PWM object


方法
------------

.. method:: PWM.init(freq, duty)

初始化PWM，freq、duty如上所述。    


示例::

 pwm.init(1000, 500)


.. method:: PWM.freq([freq_val])

当没有参数时，函数获得并返回PWM频率。当设置参数时，函数用来设置PWM频率，无返回值。

 - ``freq_val`` PWM波频率,0 < freq ≤ 0x0001312D（十进制：0 < freq ≤ 78125）

示例::

 print(pwm.freq())
 print(pwm.freq(2000)

.. method:: PWM.duty([duty_val])

没有参数时，函数获得并返回PWM占空比。有参数时，函数用来设置PWM占空比。

- ``duty_val`` 占空比, 0 ≤ duty ≤ 0x03FF（十进制：0 ≤ duty_val ≤ 1023）

示例::

 >>> print(pwm.duty())
 50
 >>> print(pwm.duty(500))
 None


.. method:: PWM.deinit( )

关闭PWM。 

