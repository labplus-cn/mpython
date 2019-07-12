
.. module:: sdcard
   :synopsis: SD卡

:mod:`sdcard` --- SD卡
==================================================

安全数字或SD卡和微型microSD卡价格低廉，可为设备增加大量存储空间。MicroPython，只有1M的闪存来存储代码和数据。
如果你拥有更大的闪存空间,可以将micro SD卡通过SPI通讯方式连接到掌控板来扩展其存储空间。


.. figure:: https://www.digikey.com/maker-media/520920e2-79cd-4b23-8e89-1acc572496e8
    :width: 400
    :align: center

    SD卡

SDCard类
-------------

.. Class:: SDCard(spi, cs)

创建SDCard对象,初始化SD卡。

- ``spi`` - machine.SPI对象
- ``cs``  _ SPI的CS控制引脚



.. literalinclude:: /../examples/file/sdcard.py
    :caption: 示例-挂载SD卡
    :linenos:



 