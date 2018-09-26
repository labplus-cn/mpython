display-oled显示
======================================

掌控板板载1.3英寸OLED显示屏，分辨率128x64。采用Google Noto Sans CJK 16x16字体，支持简体中文，繁体中文，日文和韩文语言。


.. Hint::

  display为 ``machine.framebuf`` 衍生类，所以继承framebuf的方法，详细使用可查阅。


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









