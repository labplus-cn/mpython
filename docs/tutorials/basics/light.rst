光线传感器
=============

掌控板板载光线传感器，可以用其感知周边环境的光线变化。

例：声光控灯::

    from mpython import * 

    while True:
        oled.fill(0)   #清屏
        oled.DispChar("亮度:",0,16)    #显示亮度到0，16
        oled.text("%d" % (light.read()), 48, 18)  #显示板载光线传感器
        oled.show()     #刷新
        sleep_ms(100) #延时100ms
        
        if light.read() < 200 :
            rgb[0] = (255,0,0)    # 设置红色
            rgb[1] = (0,255,0)  # 设定为绿色
            rgb[2] = (0,0,255)   # 设置为蓝色
            rgb.write()
        else: 
            rgb[0] = (0,0,0)    
            rgb[1] = (0,0,0)  
            rgb[2] = (0,0,0)   
            rgb.write()


我们使用 ``light`` 对象来获取光线传感器数据::

    >>> from mpython import *
    >>> light.read()
    >>> 432

.. Note::

    光线传感器使用 ``read()`` 函数来读取数据。返回的值为12bit的ADC采样数据，即最大值为十进制4095。


学会了如何收集周边环境的光线数据，我们可以结合其他功能做更多有趣的场景。

