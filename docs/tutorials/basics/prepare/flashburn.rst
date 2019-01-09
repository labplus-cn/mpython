烧录固件
====================


烧录工具使用乐鑫官网提供的下载软件 :download:`ESPFlashDownloadTool </../docs/tools/FLASH_DOWNLOAD_TOOLS_V3.6.4.rar>`

掌控板固件发布:https://github.com/labplus-cn/mPython/tree/master/firmware

---------

选择 **ESP32 DownloadTool** 

.. image:: /images/flashburn/flashDownload_1.png

选择 **SPIDownload** ，然后浏览并选中刚下载的掌控板固件mpython_firmware_1.0.bin，并设置地址是0x1000。浏览并选中字库Noto_Sans_CJK_SC_Light16.xbf，并设置0x300000。
将CrystallFreq设为40M，SPI SPEED 设为40MHz，SPI MODE设为DIO，FLASH SIZE改为64MBit，串口号设置为实际串口，波特率1152000。

.. image:: /images/flashburn/flashDownload_2.png

点击START，掌控板同时按下a，b键持续2秒后松开，此时掌控板将进入Download模式。固件下载中，如下图。

.. image:: /images/flashburn/flashDownload_3.png

下载完成后，如下图。

.. image:: /images/flashburn/flashDownload_4.png
