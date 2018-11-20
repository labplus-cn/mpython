oled显示
======================================

掌控板板载1.3英寸OLED显示屏，分辨率128x64。采用Google Noto Sans CJK 16x16字体，支持简体中文，繁体中文，日文和韩文语言。



.. Hint::

  display为 ``machine.framebuf`` 衍生类，所以继承framebuf的方法，详细使用可查阅  :meth:`framebuf`。


文本显示
-------

使用前，导入mpython模块::

  >>> from mpython import *
  >>> 


文本显示::

  >>> display.DispChar('hello,world!',0,0)
  >>> display.show()
  >>>

.. Note::

  DispChar(str,x,y)函数可以将左上角为坐标的文本将写入FrameBuffer。``str`` 为显示文本内容，支持简体中文，繁体中文，日文和韩文语言。``x`` ``y`` 为oled
  显示起始xy坐标。display.show()为将FrameBuffer送至oled刷新并显示屏幕。

清屏::

   >>> display.fill(1)  
   >>> display.show()
   >>> display.fill(0)
   >>> display.show()

.. Note::

  fill()为填充整个FrameBuffer区域。可以使用fill(0)来清空显示屏。同理,fill(1)可以将整屏像素点亮。


接下来,你可以尝试下在oled屏其他位置上显示中文或其他语言文本。

hello word多种字体显示示例::

  from mpython import *

  #oled
  display.DispChar('你好世界', 38, 0)
  display.DispChar('hello,world', 32, 16)
  display.DispChar('안녕하세요', 35, 32)
  display.DispChar('こんにちは世界', 24, 48)
  display.show()

.. image:: /images/掌控-正面.png


绘制线条
-------

oled还可绘制一些点、直线、矩形形状。

像素点显示::

  >>> display.pixel(50,0)     #返回(50,0)像素点的值
  0                          
  >>> display.pixel(50,0,1)   #将(50,0)像素点置为1，点亮
  >>> display.show()          #刷新显示屏

.. Note::

  display.pixel(x, y [,c ] )  ``x`` , ``y`` 为点坐标(x,y)。当如果未给出c，则获取指定像素的颜色值。
  如果给出c，则将指定的像素设置为给定的颜色。


画线::

  >>> display.hline(0,1,20,1)  #画水平线,起始点坐标(0,1),线长20
  >>> display.show()
  >>> display.vline(10,10,20,1)  #画垂直线,起始点坐标(10,10),线长20
  >>> display.show()
  >>> display.line(15,15,80,20,1)  #画起始坐标(15,15),终点坐标(80,20)方向的线
  >>> display.show()

.. Note::

  * display.hline(x, y, w, c ) 可以绘制水平线  ``x`` , ``y`` 为点坐标(x,y), ``w`` 为线宽。``c`` 为颜色值。当为1时，像素点点亮，为0则否。
  * display.vline(x, y, l, c ) 可以绘制垂直线，方法同上。
  * display.line(x1, y1, x2, y2, c) 可以绘制任意方向的线，起始坐标(x1, y1),终点坐标(x2, y2), ``c`` 为颜色值。


画矩形::

  >>> display.rect(60,25,30,25,1)   #绘制起始坐标(60, 25),宽30，高25的矩形  
  >>> display.show()
  >>> display.fill_rect(100,25,20,25,1)   #绘制起始坐标(100, 25),宽20,高25填充满颜色的矩形  
  >>> display.show()

.. Note::

  * display.rect(x, y, w, h, c)用于绘制矩形外框。起始坐标为(x, y),宽度 ``w`` , 高度 ``h`` 的矩形外框。``c`` 为颜色值。
  * display.fill_rect(x, y, w, h, c)用于绘制填充颜色的矩形，方法与rect()相同。不同于rect()只绘制矩形外框。


绘制线条例子 :download:`drawline.py </../examples/1.显示屏/drawline.py>` ::

  from mpython import *
  import time

  def testdrawline():
    for i in range(0,64):
      display.line(0,0,i*2,63,1)
      display.show()
    for i in range(0,32):
      display.line(0,0,127,i*2,1)
      display.show()
    time.sleep_ms(250)
    display.fill(0)
    display.show()
    for i in range(0,32):
      display.line(0,63,i*4,0,1)
      display.show()
    for i in range(0,16):
      display.line(0,63,127,(64-4*i)-1,1)
      display.show()
    time.sleep_ms(250)
    display.fill(0)
    display.show()
    for i in range(1,32):
      display.rect(2*i,2*i,(128-4*i)-1,(64-2*i)-1,1)
      display.show()

  testdrawline()

.. image:: /images/tutorials/drawline.gif
   :scale: 100 %

显示图片
-------

首先我们需要将图像处理为大小128*64,bmp格式颜色深度为1或者就是黑白模式。你可以使用Photoshop或者其他的图像处理软件。

接下来是使用取模工具对图片进行取模。网上有PCtoLCD、lcd image converter等取模软件，可根据自己喜好自行选择。以下使用的是 :download:`Img2Lcd工具 </../docs/tools/Image2Lcd.zip>` 。

* 步骤1.导入128x64,bmp格式图片
* 步骤2.选择参数,输出数据类型[C语言数组]、  扫描模式[水平扫描]、输出灰度[单色]、宽高[128*64]
* 步骤3.保存数据

.. image:: /images/tutorials/image2lcd.png


将取模数据赋值给bmp数组中,创建 ``framebuf`` 对象用于存储图片帧数据。然后使用 ``display.blit()`` 绘制图片至oled。

:download:`bmp.py </../examples/1.显示屏/bmp.py>` ::

  from mpython import *
  import framebuf

  #图片bitmap数组
  bmp = bytearray([\
  0X00,0X00,0X00,0X00,0X03,0XC7,0XFC,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
  0X00,0X00,0X00,0X00,0X1E,0XFF,0XFC,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
  0X00,0X00,0X00,0X31,0X70,0X3F,0XFC,0X00,0X00,0X00,0X03,0XE0,0X00,0X00,0X00,0X00,
  0X00,0X00,0X01,0XC2,0XB8,0X1F,0XF8,0X00,0X00,0X00,0X1F,0XF9,0X00,0X00,0X00,0X00,
  0X00,0X18,0X00,0XF2,0X7C,0X1F,0XF0,0X00,0X30,0X01,0XFF,0XFF,0XFF,0XE0,0X00,0X00,
  0X00,0XFF,0XFF,0XEF,0XCE,0X3F,0X80,0X01,0XFE,0X3F,0XBF,0XFF,0XFF,0XFF,0XE0,0X00,
  0X03,0XFF,0XFF,0XFF,0X1E,0X3E,0X1C,0X01,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X00,
  0X03,0XFF,0XFF,0XF8,0X0C,0X38,0X00,0X07,0XBF,0XFF,0XFF,0XFF,0XFF,0XFF,0XF8,0X00,
  0X0F,0XFF,0XFF,0XF0,0X60,0X18,0X00,0X0F,0XBF,0XFF,0XFF,0XFF,0XFF,0XFE,0X70,0X00,
  0X0C,0X0F,0XFF,0XE0,0XF8,0X00,0X00,0X07,0X9F,0XFF,0XFF,0XFF,0XFF,0XE0,0X40,0X00,
  0X10,0X0F,0XFF,0XF0,0XF8,0X00,0X00,0XC7,0X3F,0XFF,0XFF,0XFF,0XFF,0XC0,0X60,0X00,
  0X00,0X0F,0XFF,0XF9,0XFC,0X00,0X01,0X47,0XFF,0XFF,0XFF,0XFF,0XFF,0XE0,0X20,0X00,
  0X00,0X0F,0XFF,0XFB,0XFC,0X00,0X01,0X6F,0XFF,0XFF,0XFF,0XFF,0XFF,0XF8,0X00,0X00,
  0X00,0X0F,0XFF,0XFF,0XC4,0X00,0X00,0X3F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0X00,0X00,
  0X00,0X0F,0XFF,0XFF,0XC6,0X00,0X00,0X7F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0X00,0X00,
  0X00,0X0F,0XFF,0XFF,0XE0,0X00,0X00,0X3F,0XF9,0XF3,0XFF,0XFF,0XFF,0XFC,0X00,0X00,
  0X00,0X1F,0XFF,0XFF,0X00,0X00,0X01,0XF2,0XF8,0X33,0XFF,0XFF,0XFF,0XF8,0X00,0X00,
  0X00,0X3F,0XFF,0XFE,0X00,0X00,0X01,0XE1,0XBF,0XB9,0XFF,0XFF,0XFF,0XF0,0X00,0X00,
  0X00,0X3F,0XFF,0XF8,0X00,0X00,0X03,0XC0,0XA7,0XF9,0XFF,0XFF,0XFF,0X10,0X00,0X00,
  0X00,0X3F,0XFF,0XF0,0X00,0X00,0X01,0X8C,0X07,0XFD,0XFF,0XFF,0XFF,0XC8,0X00,0X00,
  0X00,0X3F,0XFF,0XF0,0X00,0X00,0X00,0XFC,0X00,0XFF,0XFF,0XFF,0XFF,0XC8,0X00,0X00,
  0X00,0X1F,0XFF,0XC0,0X00,0X00,0X03,0XFE,0X20,0XFF,0XFF,0XFF,0XFF,0XC0,0X00,0X00,
  0X00,0X1F,0XFF,0X80,0X00,0X00,0X03,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XE0,0X00,0X00,
  0X00,0X17,0XE0,0X80,0X00,0X00,0X07,0XFF,0XFF,0XFD,0XFF,0XFF,0XFF,0XE0,0X00,0X00,
  0X00,0X07,0XC0,0X80,0X00,0X00,0X0F,0XFF,0XFF,0X7C,0X7F,0XFF,0XFF,0XE0,0X00,0X00,
  0X00,0X0B,0XC0,0X00,0X00,0X00,0X0F,0XFF,0XFF,0X7F,0X83,0XFF,0XFF,0XD0,0X00,0X00,
  0X00,0X01,0XC0,0X40,0X00,0X00,0X1F,0XFF,0XFF,0XBF,0XC3,0XFF,0XFF,0X80,0X00,0X00,
  0X00,0X03,0XCC,0X28,0X00,0X00,0X1F,0XFF,0XFF,0X9F,0XC0,0XF8,0XFC,0X00,0X00,0X00,
  0X00,0X00,0XF8,0X08,0X00,0X00,0X1F,0XFF,0XFF,0XDF,0X80,0XF0,0X7C,0X08,0X00,0X00,
  0X00,0X00,0X1E,0X00,0X00,0X00,0X1F,0XFF,0XFF,0XCE,0X00,0XE0,0X3E,0X08,0X00,0X00,
  0X00,0X00,0X0E,0X00,0X00,0X00,0X1F,0XFF,0XFF,0XF8,0X00,0X60,0X1E,0X08,0X00,0X00,
  0X00,0X00,0X02,0X10,0X00,0X00,0X1F,0XFF,0XFF,0XF2,0X00,0X60,0X06,0X04,0X00,0X00,
  0X00,0X00,0X03,0X3F,0X00,0X00,0X0F,0XFF,0XFF,0XFE,0X00,0X20,0X10,0X06,0X00,0X00,
  0X00,0X00,0X00,0X7F,0X80,0X00,0X07,0XFF,0XFF,0XFE,0X00,0X10,0X10,0X02,0X00,0X00,
  0X00,0X00,0X00,0X7F,0XF0,0X00,0X03,0XCF,0XFF,0XFC,0X00,0X00,0X08,0X30,0X00,0X00,
  0X00,0X00,0X00,0X7F,0XF0,0X00,0X00,0X03,0XFF,0XF8,0X00,0X00,0X18,0X60,0X00,0X00,
  0X00,0X00,0X00,0XFF,0XF8,0X00,0X00,0X03,0XFF,0XF0,0X00,0X00,0X18,0XE0,0X00,0X00,
  0X00,0X00,0X00,0XFF,0XFE,0X00,0X00,0X03,0XFF,0XE0,0X00,0X00,0X0C,0XE8,0X40,0X00,
  0X00,0X00,0X00,0XFF,0XFF,0X80,0X00,0X03,0XFF,0XE0,0X00,0X00,0X0C,0XE8,0X3C,0X00,
  0X00,0X00,0X00,0XFF,0XFF,0XE0,0X00,0X01,0XFF,0XC0,0X00,0X00,0X04,0X00,0X0E,0X00,
  0X00,0X00,0X00,0XFF,0XFF,0XE0,0X00,0X01,0XFF,0XC0,0X00,0X00,0X01,0XC0,0X0F,0X00,
  0X00,0X00,0X00,0X7F,0XFF,0XE0,0X00,0X01,0XFF,0XC0,0X00,0X00,0X00,0X00,0X00,0X00,
  0X00,0X00,0X00,0X3F,0XFF,0XC0,0X00,0X01,0XFF,0XE0,0X00,0X00,0X00,0X00,0X40,0X00,
  0X00,0X00,0X00,0X3F,0XFF,0XC0,0X00,0X01,0XFF,0XE2,0X00,0X00,0X00,0X00,0XE4,0X00,
  0X00,0X00,0X00,0X1F,0XFF,0XC0,0X00,0X01,0XFF,0XE6,0X00,0X00,0X00,0X07,0XE4,0X00,
  0X00,0X00,0X00,0X0F,0XFF,0XC0,0X00,0X01,0XFF,0X8C,0X00,0X00,0X00,0X0F,0XFE,0X00,
  0X00,0X00,0X00,0X07,0XFF,0X80,0X00,0X01,0XFF,0X0C,0X00,0X00,0X00,0X1F,0XFE,0X00,
  0X00,0X00,0X00,0X07,0XFF,0X80,0X00,0X00,0XFF,0X8C,0X00,0X00,0X00,0X7F,0XFF,0X00,
  0X00,0X00,0X00,0X07,0XFE,0X00,0X00,0X00,0XFF,0X08,0X00,0X00,0X00,0XFF,0XFF,0X00,
  0X00,0X00,0X00,0X07,0XFC,0X00,0X00,0X00,0XFE,0X00,0X00,0X00,0X00,0XFF,0XFF,0X00,
  0X00,0X00,0X00,0X07,0XFC,0X00,0X00,0X00,0X7E,0X00,0X00,0X00,0X00,0XFF,0XFF,0X00,
  0X00,0X00,0X00,0X07,0XF8,0X00,0X00,0X00,0X7C,0X00,0X00,0X00,0X00,0XFF,0XFF,0X00,
  0X00,0X00,0X00,0X07,0XF8,0X00,0X00,0X00,0X78,0X00,0X00,0X00,0X00,0XF1,0XFE,0X00,
  0X00,0X00,0X00,0X07,0XE0,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X80,0X7C,0X00,
  0X00,0X00,0X00,0X07,0XF0,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X78,0X02,
  0X00,0X00,0X00,0X03,0XC0,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X02,
  0X00,0X00,0X00,0X03,0X80,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X20,0X08,
  0X00,0X00,0X00,0X03,0XC0,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X10,
  0X00,0X00,0X00,0X03,0X80,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X40,
  0X00,0X00,0X00,0X03,0XC0,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
  0X00,0X00,0X00,0X01,0X80,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
  0X00,0X00,0X00,0X00,0XC0,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
  0X00,0X00,0X00,0X00,0X60,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
  0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
  ])

  fb1 = framebuf.FrameBuffer(bmp,128,64, framebuf.MONO_HLSB)   #创建128x64大小帧缓存区储存图片帧，水平扫描
  #display.invert(1)     #bit反向
  display.blit(fb1,0,0)  #将fb1帧缓存送至oled显示，起始位(0,0)
  display.show()         #刷新显示屏


.. admonition:: 构建帧缓存对象 framebuf.FrameBuffer(buffer, width, height, format, stride=width) 

    - ``buffer`` - 为缓存区数据
    - ``width`` - 宽度
    - ``height`` - 高度
    - ``format`` - FrameBuffer的格式

      -  ``framebuf.MONO_HLSB`` - 定义1字节的bit位对应 **水平方向** 的像素点
      -  ``framebuf.MONO_VLSB`` - 定义1字节的bit位对应 **垂直方向** 的像素点

    - ``stride`` - 水平线的像素数, 默认为width

.. admonition:: oled显示图片帧 display.blit(fbuf, x, y)

  - ``fbuf`` - FrameBuffer对象
  - ``x，y`` - 起始点坐标（x, y）


.. image:: /images/tutorials/earth.png
   :scale: 50 %



动态显示
-------

结合上面静止帧的显示，要做到动态显示。可以将显示图片分割成每帧，送至oled逐帧显示。这样就有动态效果啦！

与上面使用.bmp格式图片不同。本次使用.pbm(Portable BitMap)格式图片，你可以使用Photoshop转换至pbm格式。

Portable Bitmap 格式
````````

pbm数据格式的前三行定于为图像标注。然后才是图像数据。第一行表示图像格式，第二行是注释，通常是用于创建它的程序。第三行是图像尺寸。
后面的才是我们需要的图像数据。数据存储每像素bit流，``1`` 表示像素点打开，``0`` 表示像素点关闭。

pbm数据格式::

  P4
  #CREATOR：GIMP PNM过滤器版本1.1
  128 64
  <数据>

首先将预先准备好的每帧的 :download:`scatman.x.pbm </../examples/display/素材/scatman.zip>`  图片上传至掌控板上。

在程序中使用 ``file.read()`` 逐帧读取图像数据流。注意，前三行不是我们需要的数据，使用 ``readlines()`` 将它舍弃。
每帧数据流创建FrameBuffer对象，将所有帧缓存储存至images列表。然后逐帧显示至oled屏。

:download:`scatman.py </../examples/1.显示屏/素材/scatman.zip>` ::

  from mpython import *
  import framebuf,time

  images = []        #创建数组列表用于存储图片帧
  for n in range(1,7):
      with open('scatman.%s.pbm' % n, 'rb') as f:
          f.readline() # Magic number
          f.readline() # Creator comment
          f.readline() # Dimensions
          data = bytearray(f.read())
      fbuf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)
      images.append(fbuf)     #将每帧数据赋值到列表

  display.invert(1)  #像素点bit反转
  while True:
      for i in images:
          display.blit(i, 0, 0)
          display.show()
          time.sleep(0.1)



.. image:: /images/tutorials/scatman.gif



























