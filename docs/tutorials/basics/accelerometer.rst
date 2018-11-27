加速度
======================================

加速度传感器能够测量由于重力引起的加速度，传感器在加速过程中，通过对质量块所受惯性力的测量，利用牛顿第二定律获得加速度值。掌控板上的加速度计可测量加速度，测量范围为 -2g 到 +2g 之间。

掌控板的测量沿3个轴，每个轴的测量值是正数或负数，正轴越趋近重力加速度方向，其数值往正数方向增加，反之往负数方向减小，当读数为 0 时，表示沿着该特定轴“水平”放置。

* X - 向前和向后倾斜。
* Y - 向左和向右倾斜。
* Z - 上下翻转。

.. image:: /images/tutorials/xyz.png
    :align: center

例：掌控体感灯（显示板载加速度传感器的值）
::
    from mpython import *
    
    while True:
        oled.fill(0)     
        x1 = accelerometer.get_x()
        y1 = accelerometer.get_y()
        z1 = accelerometer.get_z()
        oled.DispChar("加速度x:", 0, 0)
        oled.DispChar(str(x1), 48, 0)
        oled.DispChar("加速度y:", 0, 16)
        oled.DispChar(str(y1), 48, 16)
        oled.DispChar("加速度z:", 0, 32)
        oled.DispChar(str(z1), 48, 32)
        oled.show()
        if x1 > 0.5:                 # 掌控板向后倾斜
            rgb.fill((255, 0, 0))    # 设置红色灯 
            rgb.write()
        elif x1 < -0.5:              # 掌控板向前倾斜
            rgb.fill((0, 255, 0))    # 设置绿色灯 
            rgb.write()
        elif y1 > 0.5:               # 掌控板向左倾斜
            rgb.fill((0, 0, 255))    # 设置蓝色灯 
            rgb.write()
        elif y1 < -0.5:              # 掌控板向右倾斜
            rgb.fill((255, 255, 0))  # 设置黄色灯   
            rgb.write()
        elif z1 > 0.5:               # 掌控板向下翻转
            rgb.fill((0, 0, 0))      # 关闭灯     
            rgb.write()
        elif z1 < -0.5:              # 掌控板向上翻转
            rgb.fill((255, 0, 255))  # 设置紫红色灯     
            rgb.write()     


使用前，导入mpython模块::

  from mpython import *

获取X、Y、Z三轴的加速度::

    x1 = accelerometer.get_x()
    y1 = accelerometer.get_y()
    z1 = accelerometer.get_z()

.. Note::

    通过 accelerometer.get_x() 获取3轴加速度。获取3轴加速度获取方法分别为 ``get_x()`` 、``get_y()`` 、``get_z()`` 。
    每个轴的测量值根据方向是正数或负数，表示以克为单位的值。

您可以尝试掌控板按以下放置，观察3轴数据:

* 平放桌面       --(0,0,-1)
* 翻转平放桌面   --(0,0,1)
* 掌控板下板边直立与桌面 --(1,0,0) 
* 掌控板左板边直立与桌面 --(0,1,0) 

.. Note::

    发现什么规律没有？当重力加速度与加速度轴方向一致时，即等于1g的地球重力加速度。正方向为+1g，反方向为-1g。
    假如您猛烈地摇动掌控板，你会看到加速度达到±2g。那是因为这个加速度计的最大测量值为±2g。


通过测量由于重力引起的加速度，您还可以计算出设备相对于水平面的倾斜角度。

例：通过y轴加速度求y轴与水平面倾斜角度
::
    from mpython import*
    from math import acos,degrees

    while True:
        x=accelerometer.get_x()
        if x<=1 and x>=-1:
            rad_x=acos(x)
            deg_x=90-degrees(rad_x)
            oled.DispChar('%.2f°' %deg_x,50,25)
            oled.show()
            oled.fill(0)


使用前，导入mpython模块::

  from mpython import *

导入数学运算math模块中acos函数和degrees函数::

  from math import acos,degrees
  




.. Note::

    * acos() 返回x的反余弦弧度值。
    * degrees() 将弧度转换为角度。