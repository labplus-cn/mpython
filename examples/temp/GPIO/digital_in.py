# digital_in.py
# 本示例演示数字输入。
# 实验代码：按键按下（引脚数字输入状态），点亮一个灯，否则灯灭

from machine import Pin
import time

button_pin = Pin(22,  Pin.IN)
led_pin = Pin(16, Pin.OUT)

while True:
  if button_pin.value() == 1:
    led_pin.value(1)
  else:
    led_pin.value(0)
  time.sleep_us(100)
