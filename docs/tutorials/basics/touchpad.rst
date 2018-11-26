触摸按键
=======

在掌控板正面金手指处拓展6个触摸按键，依次P、Y、T、H、O、N。


例：触摸不同按键，点亮不同色RGB灯。
::
  from mpython import *

  while True:
      if(touchPad_P.read() < 100): 
          rgb[0] = (255,0,0)    # 开灯，设置红色
          rgb[1] = (255,0,0)  # 设定为红色
          rgb[2] = (255,0,0)   # 设置为红色
          rgb.write()            
      elif(touchPad_Y.read() < 100):    
          rgb[0] = (0,255,0) #关灯   
          rgb[1] = (0,255,0)  
          rgb[2] = (0,255,0)   
          rgb.write()                     
      elif(touchPad_T.read() < 100):    
          rgb[0] = (0,0,255) #关灯   
          rgb[1] = (0,0,255)  
          rgb[2] = (0,0,255)   
          rgb.write()
      elif(touchPad_H.read() < 100):    
          rgb[0] = (255,255,0) #关灯   
          rgb[1] = (255,255,0)  
          rgb[2] = (255,255,0)   
          rgb.write()
      elif(touchPad_O.read() < 100):    
          rgb[0] = (255,0,255) #关灯   
          rgb[1] = (255,0,255)  
          rgb[2] = (255,0,255)   
          rgb.write() 
      elif(touchPad_N.read() < 100):    
          rgb[0] = (0,255,255) #关灯   
          rgb[1] = (0,255,255)  
          rgb[2] = (0,255,255)   
          rgb.write()   
        

首先导入 mpython模块，尝试用手指触摸P金手指处，使用 ``read()`` 读取值。观察变化::

  >>> from mpython import *
  >>> touchPad_P.read()
  643
  >>> touchPad_P.read()
  8

.. Note::

  掌控板板载6个触摸焊盘，依次从左到右分别touchPad_P、touchPad_Y、touchPad_T、touchPad_H、touchPad_O、touchPad_N，其他触摸按键使用方法同上。

.. image:: /images/掌控板引脚定义-正面.png