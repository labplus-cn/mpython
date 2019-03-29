.. _extboard_introduce:

掌控拓展板介绍
======

概述
----

掌控拓展板是mPython掌控板衍生的一款体积小巧、易于携带。支持电机驱动、语音播放、语音合成等功能的IO引脚扩展板,可扩展12路IO接口和2路I2C接口。

.. image:: /images/extboard/extboard.png


技术参数
-------

该板具有以下特性:

    - 驱动工作电压：3.6 ～ 5.2V
    - 两路DC马达驱动,单路电流150mA
    - 支持音频功放和喇叭输出(掌控板P8，P9引脚)
    - 支持文字转语音(Text To Speech)的语音合成
    - 扩展12路IO接口、2路I2C接口
    - 体积小巧、便携,易于携带
    - 支持锂电池供电和外接USB电源供电两种方式
    - 内置350mAH锂电池,支持锂电池循环充电
    - 工作电压:3.3V
    - 最大输出电流: `1A@3.3V`
    

说明
------

.. image:: /images/extboard/layout.png
    :scale: 70 %
    :align: center

- *电源指示灯状态:3.3V输出,指示灯亮;无输出则灭*
- *充电指示灯状态:充电中,指示灯亮;充满,指示灯熄灭.(注意:只能在开关打开下,才能指示充电状态)*


.. admonition:: 扩展引脚

    拓展板扩展引脚有P0、P1、P2、P3、P5、P6、P7、P11、P13、P14、P15、P16、P19(SCL)、P20(SDA)


掌控拓展板 ``motor`` 模块: https://github.com/labplus-cn/mPython-lib



