display-oled显示
======================================

掌控板板载1.3英寸OLED显示屏，分辨率128x64。采用Google Noto Sans CJK 16x16字体，支持简体中文，繁体中文，日文和韩文语言。


.. Hint::

  display为 ``machine.framebuf`` 衍生类，所以继承framebuf的方法，详细使用可查阅  :meth:`framebuf`。


文本显示
-------

使用前，导入mPython模块::

  >>> from mPython import*
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

  from mPython import*

  #oled
  display.DispChar('你好世界', 38, 0)
  display.DispChar('hello,world', 32, 16)
  display.DispChar('안녕하세요', 35, 32)
  display.DispChar('こんにちは世界', 24, 48)
  display.show()


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


以下是绘制线条例子::

  from mPython import *
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












































