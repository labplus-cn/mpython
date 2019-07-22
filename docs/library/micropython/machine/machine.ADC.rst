.. currentmodule:: machine
.. _machine.ADC:

.. module:: ADC

类 ADC -- 模数转换
=========================================


构建对象
------------

.. class:: ADC(Pin)

创建与设定引脚关联的ADC对象。这样您就可以读取该引脚上的模拟值。

 - ``Pin`` - ADC在专用引脚上可用，ESP32可用引脚有：IO39、IO36、IO35、IO33、IO34、IO32。掌控板的ADC引脚有P0、P1、P2、P3、P4、P10。

详细引脚定义可查阅 `ESP32引脚功能表. <../../../_images/pinout_wroom_pinout.png>`_ 和  :ref:`掌控板引脚定义<mpython_pinout>` 章节。


示例::

      from machine import ADC, Pin

      adc = ADC(Pin(33))      # create an ADC object


方法
-------

.. method:: ADC.read( )

   读取ADC并返回读取结果。




.. method:: ADC.atten(db)

    该方法允许设置ADC输入的衰减量。这允许更宽的可能输入电压范围，但是以精度为代价（相同的位数现在表示更宽的范围）。在未设置atten(),默认为0DB衰减。可能的衰减选项包括：
    
    - ``db``
 

        =================== ========== ======= ====================================  
        宏定义                衰减量     数值     满量程电压
        =================== ========== ======= ==================================== 
        ``ADC.ATTN_0DB``     0dB衰减     0      1V
        ``ADC.ATTN_2_5DB``   2.5dB衰减   1      1.5V
        ``ADC.ATTN_6DB``     6dB衰减     2      2V
        ``ADC.ATTN_11DB``    11dB衰减    3      3.3V
        =================== ========== ======= ==================================== 

.. method:: ADC.width(bit)

    设置数据宽度(分辨率)。ADC的分辨率是指能够将采集的模拟信号转化为数字信号的精度，通常我们用“位”来表述，比如8位就是指ADC可以将制定量程内的电压信号，分别对应到0 - 2^8-1,即 0-255这256个数字上。分辨率位数越高，能够表示的也就越精确，信息丢失的也就越少。
    
    - ``bit`` -  宽度选项有:

        =================== ========== =============
        宏定义                数值        满量程   
        =================== ========== =============
        ``ADC.WIDTH_9BIT``    0         0x1ff(511)
        ``ADC.WIDTH_10BIT``   1         0x3ff(1023)
        ``ADC.WIDTH_11BIT``   2         0x7ff(2047)
        ``ADC.WIDTH_12BIT``   3         00xfff(4095)
        =================== ========== =============

示例::

      from machine import ADC, Pin

      adc = ADC(Pin(34))      # create an ADC object
      adc.atten(adc.ATTN_11DB)   # set 3.3V Range
      x = adc.read()
      print(x)

常量
---------


衰减比
````````
.. data:: ADC.ATTN_0DB


.. data:: ADC.ATTN_2_5DB


.. data:: ADC.ATTN_6DB



.. data:: ADC.ATTN_11DB


数据宽度
````````
.. data:: ADC.WIDTH_9BIT



.. data:: ADC.WIDTH_10BIT



.. data:: ADC.WIDTH_11BIT



.. data:: ADC.WIDTH_12BIT







