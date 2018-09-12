.. _neopixel:
:mod:`neopixel` --- WS2812 灯带
=========================================

NeoPixels也被称为WS2812 LEDs，是连接在一起的全彩色led串行、单独寻址，并可以设置他它们的红色，绿色和蓝色
在0到255之间。它们需要精确的时间来控制它们有一个特殊的neopixel模块来做这个。

构建函数
------------

.. class:: NeoPixel(pin, n,bpp=3,timing=0)

  - ``pin`` :输出引脚
  -  ``n`` :LED灯的个数
  - ``bpp``:每个RGB灯bytearray数组数量，默认为3
  - ``timing``:默认等于0,为400KHz速率；等于1，为800KHz速率

示例::

  from machine import Pin
  import neopixel

  pin = Pin(17, Pin.OUT)
  np = neopixel.NeoPixel(pin, bpp=3,timing=1)   #800khz

方法
-------

.. method:: NeoPixel.write()

把数据写入LED中。 

示例::

  np[0] = (255, 255, 255) # 设置第一个LED像素为白色
  np.write()

.. method:: NeoPixel.fill(rgb_buf)

填充所有LED像素。

  - ``rgb_buf`` :rgb颜色

示例::

  np.fill( (255, 255, 255) )

