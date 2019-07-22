
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

首先,须确保SPI总线的引脚与micro SD卡物理连接正确。确保您的micro SD卡使用FAT或FAT32文件系统格式化。然后,用os.mount(),将SD卡虚拟新的FAT文件系统挂载到指定的目录中。
挂载完成后,你就可以使用Python 的文件操作(如打开,关闭,读取和写入)来访问文件。

- ``spi`` - machine.SPI对象
- ``cs``  - SPI的CS控制引脚


.. literalinclude:: /../examples/file/sdcard.py
    :caption: 示例-挂载SD卡
    :linenos:


.. literalinclude:: /../examples/file/print_directory.py
    :caption: 示例-列出所有文件
    :linenos:
 