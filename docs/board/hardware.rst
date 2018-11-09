硬件概述
====================

mPython掌控是一块MicroPython微控制器板，很好的支持MicroPython/Python软件上功能。

.. image:: /images/掌控-立2.png

技术参数
-----------

该板具有以下硬件特性:

  - ESP-32主控

    - 处理器：Tensilica LX6双核处理器（一核处理高速连接；一核独立应用开发）
    - 主频：高达240MHz的时钟频率
    -	SRAM：520KB
    - Flash：8MB
    - Wi-Fi标准：FCC/CE/TELEC/KCC
    - Wi-Fi协议：802.11 b/g/n/d/e/i/k/r (802.11n，速度高达150 Mbps)，A-MPDU和A-MSDU聚合，支持0.4us防护间隔
    - 频率范围：2.4~2.5 GHz
    - 蓝牙协议：符合蓝牙v4.2 BR/EDR和BLE标准
    - 蓝牙音频：CVSD和SBC音频低功耗：10uA

  - 供电方式：Micro USB供电
  - 工作电压：3.3V
  - 工作电流:100mA
  - 掌控板载

    - 三轴加速度计MSA300,测量范围:±2G
    - 光线传感器
    - 麦克风
    - 3 颗全彩ws2812灯珠
    - 1.3英寸OLED显示屏，支持16*16字符显示，分辨率128x64
    - 无源蜂鸣器
    - 支持2个物理按键(A/B)、6个触摸按键
    - 支持1路鳄鱼夹接口，可方便接入各种阻性传感器

  - 拓展接口

    - 20通道数字I/O， (其中支持18路PWM，6路触摸输入)
    - 5通道12bit模拟输入ADC，A0~A4  
    - 1路的外部输入鳄鱼夹接口:EXT/GND
    - 支持I2C、UART、SPI通讯协议


元件布局
--------------

.. image:: /images/布局-正面.png

.. image:: /images/布局-背面.png


.. _mpython_pinout:

引脚定义
--------------

.. image:: /images/掌控板引脚定义-正面.png

.. image:: /images/掌控板引脚定义-背面.png

.. image:: /images/掌控板-pinout_wroom.png


掌控板接口引脚说明
++++++++++++++++



==========  ====================================  
 引脚         描述
==========  ====================================  
 P3          模拟/数字输入,连接掌控板电阻传感器EXT
 P0          模拟/数字输入/数字输出
 P4          模拟/数字输入,连接掌控板光线传感器  
 P5          数字输入/数字输出, 连接掌控板按键A
 P6          数字输入/数字输出, 连接掌控板蜂鸣器,不使用蜂鸣器时,可以作为通用GPIO使用
 P7          数字输入/数字输出, 通过单总线控制掌控板上的3个RGB LED, 可以作为通用GPIO使用
 P1          模拟/数字输入/数字输出 
 P8          模拟/数字输入/数字输出
 P9          模拟/数字输入/数字输出
 P10         模拟/数字输入,连接掌控板声音传感器
 P11         数字输入/数字输出, 连接掌控板按键B
 P12         保留
 P2          模拟/数字输入
 P13         数字输入/数字输出
 P14         数字输入/数字输出
 P15         数字输入/数字输出
 P16         数字输入/数字输出
 3V3         电源正输入:连接USB时,掌控板内部稳压输出3.3V,未连接USB可以通过输入(2.7-3.6)V电压为掌控板供电
 P19         I2C总线SCL,与内部的OLED和加速度传感器共享I2C总线
 P20         I2C总线SDA,与内部的OLED和加速度传感器共享I2C总线
 GND         电源GND
==========  ====================================  









相关下载
--------------

原理图
++++++

* :download:`mPython掌控板V0.9原理图 </../docs/hardware/labplus_mPython_V0.9.pdf>`

主要数据手册
+++++++

* :download:`USB-to-UART Bridge：cp2104 </../docs/hardware/CP2104-SiliconLaboratories.pdf>`
* :download:`ESP32-WROOM </../docs/hardware/esp32-wroom-32_datasheet_cn.pdf>`
* :download:`LDO稳压:AP2112K-3.3 </../docs/hardware/AP2112K-3.3.PDF>`
* :download:`加速度计:MSA300 </../docs/hardware/MSA300-V1.0-ENG.pdf>`
* :download:`OLED：128x64 </../docs/hardware/1.30-SPEC QG-2864KSWLG01 VER A.pdf>`

