# bink.py
# 实现led灯闪烁

from machine import Pin
import time
# led引脚初始化
led_pin = Pin(16, Pin.OUT)
# 循环控制led亮灭
while True:
  led_pin.value(1)
  time.sleep_ms(500)
  led_pin.value(0)
  time.sleep_ms(500)
