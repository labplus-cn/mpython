# button_A_B
# 利用板载按键开关灯
from machine import Pin
import time

# led灯引脚初始化
led_pin = Pin(16, Pin.OUT)
led_pin.value(0)
# 按键引脚初始化
BTNA = Pin(25, Pin.IN)
BTNB = Pin(26, Pin.IN)

# 按键中断响应函数
def btn_A_irq(_):
  if BTNA.value() == 0:
    led_pin.value(1)
  else:
    led_pin.value(0)

def btn_B_irq(_):
  if BTNB.value() == 0:
    led_pin.value(1)
  else:
    led_pin.value(0)

# 绑定按键中断响应函数    
BTNA.irq(btn_A_irq)
BTNB.irq(btn_B_irq)
