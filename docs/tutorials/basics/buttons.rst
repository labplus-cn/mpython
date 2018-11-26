按键
======================================

在掌控板上部边沿有按压式A、B两个按键。当按下按键时为低电平，否则高电平。


例：按A键开灯，按B键关灯
::
  from mpython import *  

  while True:
      if button_a.value() == 0 and  button_b.value() == 1 :#按下时为0，松开为1        
          rgb[0] = (255,0,0)    # 设置红色
          rgb[1] = (255,0,0)  # 设定为红色
          rgb[2] = (255,0,0)   # 设置为红色
          rgb.write()        
      if button_a.value() == 1 and  button_b.value() == 0 :
          rgb[0] = (0, 0, 0)  #关灯
          rgb[1] = (0, 0, 0)
          rgb[2] = (0, 0, 0)
          rgb.write()    
      sleep_ms(100)#延时防抖


使用前，导入mpython模块::

  from mpython import *

按键 A 按下和按键 B 未按下 ::

  button_a.value() == 0      #按键 A 按下
  button_b.value() == 1      #按键 B 未按

.. Note::

  ``button_a`` 为按键 A 对象名，按键 B 对象名为 ``button_b`` ，是 ``machine.Pin`` 衍生类，继承Pin的方法，所以可使用 ``value`` 函数读取引脚值，返回 ``1`` 代表高电平信号，返回 ``0`` 代表低电平信号，因此当按键未按下状态时value==1，按下状态时value==0。


还可以使用引脚的中断处理，如当按下按键 A 打印输出::
  
  def callback(_):            #先定义中断处理函数
    print('Button a Pressed')
  button_a.irq(trigger=Pin.IRQ_FALLING, handler=callback)     #设置按键 A 中断,下降沿触发
   

可以尝试按下按键 A，在REPL—交互模式下看中断效果。当检测到按键按下，回调打印::

    >>> Button Pressed
  Button Pressed
  Button Pressed
  Button Pressed
  Button Pressed



定义中断处理函数时，函数须包含任意一个参数，否则无法使用。callback()函数中的参数为 ``_`` 。
``trigger`` 可修改触发方式，``handler`` 为中断处理函数。详细使用可查阅  :ref:`Pin.irq<Pin.irq>`。



